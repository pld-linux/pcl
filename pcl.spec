# TODO: MPI, ROS?
#
# Conditional build:
%bcond_without	apidocs	# do not build and package API docs
%bcond_without	fzapi	# Fotonic FZ API support
%bcond_with	sse	# SSE/SSE2/SSE3 support
%bcond_without	tawara	# Tawara video output (pcl_video)
%bcond_without	vtk	# VTK support in libpcl_{io,surface} + libpcl_{apps,visualization} libs

Summary:	Point Cloud Library - library for point cloud processing
Summary(pl.UTF-8):	Point Cloud Library - biblioteka do operacji na chmurze punktów
Name:		pcl
Version:	1.7.2
Release:	9
License:	BSD
Group:		Libraries
#Source0Download: http://pointclouds.org/downloads/
Source0:	https://github.com/PointCloudLibrary/pcl/archive/%{name}-%{version}.tar.gz
# Source0-md5:	02c72eb6760fcb1f2e359ad8871b9968
Patch0:		%{name}-fz_api.patch
Patch1:		%{name}-tawara.patch
Patch2:		%{name}-openni.patch
Patch3:		eigen-dependency.patch
URL:		http://pointclouds.org/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenNI-devel
BuildRequires:	OpenNI2-devel
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtOpenGL-devel >= 4
BuildRequires:	boost-devel >= 1.43
BuildRequires:	cmake >= 2.8
BuildRequires:	eigen3 >= 3
BuildRequires:	flann-devel >= 1.7.0
%{?with_fzapi:BuildRequires:	fz-api-devel}
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	libgomp-devel
BuildRequires:	libpcap-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	qhull-devel
BuildRequires:	qt4-build >= 4
BuildRequires:	python
BuildRequires:	sed >= 4.0
%{?with_tawara:BuildRequires:	tawara-devel}
# FIXME: only vtk-devel is really required, the rest (java,python,tcl runtimes) only because of checks in VTK cmake files
%{?with_vtk:BuildRequires:	vtk-devel >= 6}
%{?with_vtk:BuildRequires:	vtk-java >= 6}
%{?with_vtk:BuildRequires:	vtk-python >= 6}
%{?with_vtk:BuildRequires:	vtk-tcl >= 6}
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-sphinxcontrib-doxylink >= 1.3
BuildRequires:	sphinx-pdg >= 1.3.3-2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Point Cloud Library (PCL) is a standalone, large scale, open
project for 3D point cloud processing.

The PCL framework contains numerous state-of-the art algorithms
including filtering, feature estimation, surface reconstruction,
registration, model fitting and segmentation, as well as higher level
tools for performing mapping and object recognition. Think of it as
the Boost of 3D point cloud processing.

%description -l pl.UTF-8
Biblioteka PCL (Point Cloud Processing) to samodzielna, wielkoskalowa,
mająca otwarte źródła biblioteka do przetwarzania chmury punktów 3D.

Szkielet PCL zawiera wiele współczesnych algorytmów, obejmujących
filtrowanie, przybliżanie cech, rekonstrukcję powierzchni,
rejestrację, dopasowywanie modeli oraz segmentację, a także narzędzia
wyższego poziomu do wykonywania odwzorowań oraz rozpoznawania
obiektów. O bibliotece można myśleć jako odpowiedniku Boosta do
przetwarzania chmury punktów 3D.

%package devel
Summary:	Header files for PCL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PCL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.44
Requires:	eigen3 >= 3
%{?with_vtk:Requires:	vtk-devel >= 6}

%description devel
Header files for PCL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PCL.

%package apidocs
Summary:	PCL API documentation and tutorials
Summary(pl.UTF-8):	Dokumentacja API oraz wprowadzenie do biblioteki PCL
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation and tutorials for PCL library.

%description apidocs -l pl.UTF-8
Dokumentacja API oraz wprowadzenie do biblioteki PCL.

%prep
%setup -q -n pcl-pcl-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
mkdir build
cd build
# LIB_INSTALL_DIR specified by PLD cmake macro is incompatible with what PCL expects
%cmake .. \
	-DLIB_INSTALL_DIR=%{_lib} \
%if %{with fzapi}
	-DFZAPI_DIR=/usr \
	-DFZAPI_INCLUDE_DIR=/usr/include \
	-DFZAPI_LIBS=%{_libdir}/libfz_api.so \
%endif
%if %{with apidocs}
	-DWITH_DOCS=ON \
	-DWITH_TUTORIALS=ON \
%endif
	%{!?with_sse:-DPCL_ENABLE_SSE=OFF}

# NOTE: -j1 because of OOM on th-x86_64
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt
%attr(755,root,root) %{_bindir}/pcl_compute_hausdorff
%attr(755,root,root) %{_bindir}/pcl_compute_hull
%attr(755,root,root) %{_bindir}/pcl_concatenate_points_pcd
%attr(755,root,root) %{_bindir}/pcl_convert_pcd_ascii_binary
%attr(755,root,root) %{_bindir}/pcl_demean_cloud
%attr(755,root,root) %{_bindir}/pcl_fast_bilateral_filter
%attr(755,root,root) %{_bindir}/pcl_generate
%attr(755,root,root) %{_bindir}/pcl_grid_min
%attr(755,root,root) %{_bindir}/pcl_hdl_grabber
%attr(755,root,root) %{_bindir}/pcl_linemod_detection
%attr(755,root,root) %{_bindir}/pcl_local_max
%attr(755,root,root) %{_bindir}/pcl_lum
%attr(755,root,root) %{_bindir}/pcl_match_linemod_template
%attr(755,root,root) %{_bindir}/pcl_morph
%attr(755,root,root) %{_bindir}/pcl_ndt2d
%attr(755,root,root) %{_bindir}/pcl_ndt3d
%attr(755,root,root) %{_bindir}/pcl_obj2pcd
%attr(755,root,root) %{_bindir}/pcl_oni2pcd
%attr(755,root,root) %{_bindir}/pcl_openni_grabber_depth_example
%attr(755,root,root) %{_bindir}/pcl_openni_grabber_example
%attr(755,root,root) %{_bindir}/pcl_openni_pcd_recorder
%attr(755,root,root) %{_bindir}/pcl_outofcore_print
%attr(755,root,root) %{_bindir}/pcl_outofcore_process
%attr(755,root,root) %{_bindir}/pcl_outofcore_viewer
%attr(755,root,root) %{_bindir}/pcl_pcd_change_viewpoint
%attr(755,root,root) %{_bindir}/pcl_pcd_convert_NaN_nan
%attr(755,root,root) %{_bindir}/pcl_pclzf2pcd
%attr(755,root,root) %{_bindir}/pcl_ply2obj
%attr(755,root,root) %{_bindir}/pcl_ply2ply
%attr(755,root,root) %{_bindir}/pcl_ply2raw
%attr(755,root,root) %{_bindir}/pcl_plyheader
%attr(755,root,root) %{_bindir}/pcl_progressive_morphological_filter
%attr(755,root,root) %{_bindir}/pcl_radius_filter
%attr(755,root,root) %{_bindir}/pcl_sac_segmentation_plane
%attr(755,root,root) %{_bindir}/pcl_train_linemod_template
%attr(755,root,root) %{_bindir}/pcl_uniform_sampling
%attr(755,root,root) %{_bindir}/pcl_xyz2pcd
%if %{with vtk}
%attr(755,root,root) %{_bindir}/pcl_add_gaussian_noise
%attr(755,root,root) %{_bindir}/pcl_boundary_estimation
%attr(755,root,root) %{_bindir}/pcl_cluster_extraction
%attr(755,root,root) %{_bindir}/pcl_compute_cloud_error
%attr(755,root,root) %{_bindir}/pcl_crop_to_hull
%attr(755,root,root) %{_bindir}/pcl_elch
%attr(755,root,root) %{_bindir}/pcl_extract_feature
%attr(755,root,root) %{_bindir}/pcl_fpfh_estimation
%attr(755,root,root) %{_bindir}/pcl_gp3_surface
%attr(755,root,root) %{_bindir}/pcl_ground_based_rgbd_people_detector
%attr(755,root,root) %{_bindir}/pcl_hdl_viewer_simple
%attr(755,root,root) %{_bindir}/pcl_icp
%attr(755,root,root) %{_bindir}/pcl_icp2d
%attr(755,root,root) %{_bindir}/pcl_image_grabber_saver
%attr(755,root,root) %{_bindir}/pcl_image_grabber_viewer
%attr(755,root,root) %{_bindir}/pcl_marching_cubes_reconstruction
%attr(755,root,root) %{_bindir}/pcl_mesh2pcd
%attr(755,root,root) %{_bindir}/pcl_mesh_sampling
%attr(755,root,root) %{_bindir}/pcl_mls_smoothing
%attr(755,root,root) %{_bindir}/pcl_normal_estimation
%attr(755,root,root) %{_bindir}/pcl_obj2vtk
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_accepted_hypotheses
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_hash_table
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_model_opps
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_orr_octree
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_orr_octree_zprojection
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_result
%attr(755,root,root) %{_bindir}/pcl_obj_rec_ransac_scene_opps
%attr(755,root,root) %{_bindir}/pcl_octree_viewer
%attr(755,root,root) %{_bindir}/pcl_oni_viewer
%attr(755,root,root) %{_bindir}/pcl_openni_image
%attr(755,root,root) %{_bindir}/pcl_openni_save_image
%attr(755,root,root) %{_bindir}/pcl_openni_viewer
%attr(755,root,root) %{_bindir}/pcl_organized_pcd_to_png
%attr(755,root,root) %{_bindir}/pcl_outlier_removal
%attr(755,root,root) %{_bindir}/pcl_passthrough_filter
%attr(755,root,root) %{_bindir}/pcl_pcd2ply
%attr(755,root,root) %{_bindir}/pcl_pcd2png
%attr(755,root,root) %{_bindir}/pcl_pcd2vtk
%attr(755,root,root) %{_bindir}/pcl_pcd_grabber_viewer
%attr(755,root,root) %{_bindir}/pcl_pcd_image_viewer
%attr(755,root,root) %{_bindir}/pcl_plane_projection
%attr(755,root,root) %{_bindir}/pcl_ply2pcd
%attr(755,root,root) %{_bindir}/pcl_ply2vtk
%attr(755,root,root) %{_bindir}/pcl_png2pcd
%attr(755,root,root) %{_bindir}/pcl_poisson_reconstruction
%attr(755,root,root) %{_bindir}/pcl_registration_visualizer
%attr(755,root,root) %{_bindir}/pcl_spin_estimation
%attr(755,root,root) %{_bindir}/pcl_tiff2pcd
%attr(755,root,root) %{_bindir}/pcl_timed_trigger_test
%attr(755,root,root) %{_bindir}/pcl_transform_from_viewpoint
%attr(755,root,root) %{_bindir}/pcl_transform_point_cloud
%attr(755,root,root) %{_bindir}/pcl_vfh_estimation
%{?with_tawara:%attr(755,root,root) %{_bindir}/pcl_video}
%attr(755,root,root) %{_bindir}/pcl_viewer
%attr(755,root,root) %{_bindir}/pcl_virtual_scanner
%attr(755,root,root) %{_bindir}/pcl_voxel_grid
%attr(755,root,root) %{_bindir}/pcl_voxel_grid_occlusion_estimation
%attr(755,root,root) %{_bindir}/pcl_vtk2obj
%attr(755,root,root) %{_bindir}/pcl_vtk2pcd
%attr(755,root,root) %{_bindir}/pcl_vtk2ply
%endif
%attr(755,root,root) %{_libdir}/libpcl_common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_common.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_features.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_features.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_filters.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_filters.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_io.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_io.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_io_ply.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_io_ply.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_kdtree.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_kdtree.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_keypoints.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_keypoints.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_octree.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_octree.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_outofcore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_outofcore.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_recognition.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_recognition.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_registration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_registration.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_sample_consensus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_sample_consensus.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_search.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_search.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_segmentation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_segmentation.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_surface.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_surface.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_tracking.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_tracking.so.1.7
%if %{with vtk}
%attr(755,root,root) %{_libdir}/libpcl_people.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_people.so.1.7
%attr(755,root,root) %{_libdir}/libpcl_visualization.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_visualization.so.1.7
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcl_common.so
%attr(755,root,root) %{_libdir}/libpcl_features.so
%attr(755,root,root) %{_libdir}/libpcl_filters.so
%attr(755,root,root) %{_libdir}/libpcl_io.so
%attr(755,root,root) %{_libdir}/libpcl_io_ply.so
%attr(755,root,root) %{_libdir}/libpcl_kdtree.so
%attr(755,root,root) %{_libdir}/libpcl_keypoints.so
%attr(755,root,root) %{_libdir}/libpcl_octree.so
%attr(755,root,root) %{_libdir}/libpcl_outofcore.so
%attr(755,root,root) %{_libdir}/libpcl_recognition.so
%attr(755,root,root) %{_libdir}/libpcl_registration.so
%attr(755,root,root) %{_libdir}/libpcl_sample_consensus.so
%attr(755,root,root) %{_libdir}/libpcl_search.so
%attr(755,root,root) %{_libdir}/libpcl_segmentation.so
%attr(755,root,root) %{_libdir}/libpcl_surface.so
%attr(755,root,root) %{_libdir}/libpcl_tracking.so
%if %{with vtk}
%attr(755,root,root) %{_libdir}/libpcl_people.so
%attr(755,root,root) %{_libdir}/libpcl_visualization.so
%endif
%{_includedir}/pcl-1.7
%{_pkgconfigdir}/pcl_common-1.7.pc
%{_pkgconfigdir}/pcl_features-1.7.pc
%{_pkgconfigdir}/pcl_filters-1.7.pc
%{_pkgconfigdir}/pcl_geometry-1.7.pc
%{_pkgconfigdir}/pcl_io-1.7.pc
%{_pkgconfigdir}/pcl_kdtree-1.7.pc
%{_pkgconfigdir}/pcl_keypoints-1.7.pc
%{_pkgconfigdir}/pcl_octree-1.7.pc
%{_pkgconfigdir}/pcl_outofcore-1.7.pc
%{_pkgconfigdir}/pcl_recognition-1.7.pc
%{_pkgconfigdir}/pcl_registration-1.7.pc
%{_pkgconfigdir}/pcl_sample_consensus-1.7.pc
%{_pkgconfigdir}/pcl_search-1.7.pc
%{_pkgconfigdir}/pcl_segmentation-1.7.pc
%{_pkgconfigdir}/pcl_surface-1.7.pc
%{_pkgconfigdir}/pcl_tracking-1.7.pc
%if %{with vtk}
%{_pkgconfigdir}/pcl_people-1.7.pc
%{_pkgconfigdir}/pcl_visualization-1.7.pc
%endif
%dir %{_datadir}/pcl-1.7
%{_datadir}/pcl-1.7/PCLConfig*.cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%dir %{_docdir}/pcl-1.7
%{_docdir}/pcl-1.7/advanced
%{_docdir}/pcl-1.7/html
%{_docdir}/pcl-1.7/tutorials
%endif
