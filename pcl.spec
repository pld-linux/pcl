# TODO: MPI, ROS?
#
# Conditional build:
%bcond_without	apidocs	# do not build and package API docs
%bcond_without	vtk	# VTK support in libpcl_{io,surface} + libpcl_{apps,visualization} libs
#
Summary:	Point Cloud Library - library for point cloud processing
Summary(pl.UTF-8):	Point Cloud Library - biblioteka do operacji na chmurze punktów
Name:		pcl
Version:	1.6.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: http://pointclouds.org/downloads/
Source0:	http://www.pointclouds.org/assets/files/1.6.0/PCL-%{version}-Source.tar.bz2
# Source0-md5:	f83ca5d0ff290412b0807864b95eba26
Patch0:		%{name}-link.patch
Patch1:		%{name}-openni.patch
URL:		http://pointclouds.org/
BuildRequires:	OpenNI-devel
BuildRequires:	boost-devel >= 1.40
BuildRequires:	cmake >= 2.8
BuildRequires:	eigen3 >= 3
BuildRequires:	flann-devel
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	qhull-devel
BuildRequires:	python
BuildRequires:	sed >= 4.0
# FIXME: only vtk-devel is really required, the rest only because of checks in VTK cmake files
%{?with_vtk:BuildRequires:	vtk-devel}
%{?with_vtk:BuildRequires:	vtk-java}
%{?with_vtk:BuildRequires:	vtk-python}
%{?with_vtk:BuildRequires:	vtk-tcl}
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python-sphinxcontrib-doxylink >= 1.3
BuildRequires:	sphinx-pdg
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
%{?with_vtk:Requires:	vtk-devel}

%description devel
Header files for PCL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PCL.

%package apidocs
Summary:	PCL API documentation and tutorials
Summary(pl.UTF-8):	Dokumentacja API oraz wprowadzenie do biblioteki PCL
Group:		Documentation

%description apidocs
API documentation and tutorials for PCL library.

%description apidocs -l pl.UTF-8
Dokumentacja API oraz wprowadzenie do biblioteki PCL.

%prep
%setup -q -n PCL-%{version}-Source
%patch0 -p1
%patch1 -p1

# don't use SSE/SSE2/SSE3 just because compiler and builder host supports it
%{__sed} -i -e '/^PCL_CHECK_FOR_SSE/d' CMakeLists.txt

%build
mkdir build
cd build
# LIB_INSTALL_DIR specified by PLD cmake macro is incompatible with what PCL expects
%cmake .. \
	-DLIB_INSTALL_DIR=%{_lib}

# NOTE: -j1 because of OOM on th-x86_64
%{__make} -j1

# why it's not called on build?
%if %{with apidocs}
cd doc/doxygen
doxygen doxyfile
cd ../tutorials
sphinx-build -b html -a -d doctrees ../../../doc/tutorials/content html
%endif

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
%attr(755,root,root) %{_bindir}/pcl_convert_pcd_ascii_binary
%attr(755,root,root) %{_bindir}/pcl_openni_grabber_example
%attr(755,root,root) %{_bindir}/pcl_openni_io
%attr(755,root,root) %{_bindir}/pcl_pcd_convert_NaN_nan
%attr(755,root,root) %{_bindir}/pcl_ply2obj
%attr(755,root,root) %{_bindir}/pcl_ply2ply
%attr(755,root,root) %{_bindir}/pcl_ply2raw
%attr(755,root,root) %{_bindir}/pcl_plyheader
%if %{with vtk}
%attr(755,root,root) %{_bindir}/oni_viewer
%attr(755,root,root) %{_bindir}/openni_fast_mesh
%attr(755,root,root) %{_bindir}/openni_ii_normal_estimation
%attr(755,root,root) %{_bindir}/openni_image
%attr(755,root,root) %{_bindir}/openni_viewer
%attr(755,root,root) %{_bindir}/openni_voxel_grid
%attr(755,root,root) %{_bindir}/pcd_grabber_viewer
%attr(755,root,root) %{_bindir}/pcd_viewer
%attr(755,root,root) %{_bindir}/pcl_add_gaussian_noise
%attr(755,root,root) %{_bindir}/pcl_boundary_estimation
%attr(755,root,root) %{_bindir}/pcl_cluster_extraction
%attr(755,root,root) %{_bindir}/pcl_compute_cloud_error
%attr(755,root,root) %{_bindir}/pcl_crop_to_hull
%attr(755,root,root) %{_bindir}/pcl_elch
%attr(755,root,root) %{_bindir}/pcl_extract_feature
%attr(755,root,root) %{_bindir}/pcl_feature_matching
%attr(755,root,root) %{_bindir}/pcl_fpfh_estimation
%attr(755,root,root) %{_bindir}/pcl_gp3_surface
%attr(755,root,root) %{_bindir}/pcl_icp
%attr(755,root,root) %{_bindir}/pcl_icp2d
%attr(755,root,root) %{_bindir}/pcl_marching_cubes_reconstruction
%attr(755,root,root) %{_bindir}/pcl_mesh2pcd
%attr(755,root,root) %{_bindir}/pcl_mesh_sampling
%attr(755,root,root) %{_bindir}/pcl_mls_smoothing
%attr(755,root,root) %{_bindir}/pcl_multiscale_feature_persistence_example
%attr(755,root,root) %{_bindir}/pcl_nn_classification_example
%attr(755,root,root) %{_bindir}/pcl_normal_estimation
%attr(755,root,root) %{_bindir}/pcl_octree_viewer
%attr(755,root,root) %{_bindir}/pcl_openni_3d_concave_hull
%attr(755,root,root) %{_bindir}/pcl_openni_3d_convex_hull
%attr(755,root,root) %{_bindir}/pcl_openni_boundary_estimation
%attr(755,root,root) %{_bindir}/pcl_openni_change_viewer
%attr(755,root,root) %{_bindir}/pcl_openni_fast_mesh
%attr(755,root,root) %{_bindir}/pcl_openni_feature_persistence
%attr(755,root,root) %{_bindir}/pcl_openni_floodfill_planar_segmentation
%attr(755,root,root) %{_bindir}/pcl_openni_grab_frame
%attr(755,root,root) %{_bindir}/pcl_openni_ii_normal_estimation
%attr(755,root,root) %{_bindir}/pcl_openni_mls_smoothing
%attr(755,root,root) %{_bindir}/pcl_openni_organized_multi_plane_segmentation
%attr(755,root,root) %{_bindir}/pcl_openni_planar_convex_hull
%attr(755,root,root) %{_bindir}/pcl_openni_planar_segmentation
%attr(755,root,root) %{_bindir}/pcl_openni_save_image
%attr(755,root,root) %{_bindir}/pcl_openni_stream_compression
%attr(755,root,root) %{_bindir}/pcl_openni_tracking
%attr(755,root,root) %{_bindir}/pcl_openni_uniform_sampling
%attr(755,root,root) %{_bindir}/pcl_openni_voxel_grid
%attr(755,root,root) %{_bindir}/pcl_outlier_removal
%attr(755,root,root) %{_bindir}/pcl_passthrough_filter
%attr(755,root,root) %{_bindir}/pcl_pcd2ply
%attr(755,root,root) %{_bindir}/pcl_pcd2vtk
%attr(755,root,root) %{_bindir}/pcl_pcd_organized_multi_plane_segmentation
%attr(755,root,root) %{_bindir}/pcl_plane_projection
%attr(755,root,root) %{_bindir}/pcl_ply2pcd
%attr(755,root,root) %{_bindir}/pcl_poisson_reconstruction
%attr(755,root,root) %{_bindir}/pcl_ppf_object_recognition
%attr(755,root,root) %{_bindir}/pcl_pyramid_surface_matching
%attr(755,root,root) %{_bindir}/pcl_registration_visualizer
%attr(755,root,root) %{_bindir}/pcl_spin_estimation
%attr(755,root,root) %{_bindir}/pcl_statistical_multiscale_interest_region_extraction_example
%attr(755,root,root) %{_bindir}/pcl_surfel_smoothing_test
%attr(755,root,root) %{_bindir}/pcl_test_search_speed
%attr(755,root,root) %{_bindir}/pcl_transform_from_viewpoint
%attr(755,root,root) %{_bindir}/pcl_transform_point_cloud
%attr(755,root,root) %{_bindir}/pcl_vfh_estimation
%attr(755,root,root) %{_bindir}/pcl_virtual_scanner
%attr(755,root,root) %{_bindir}/pcl_voxel_grid
%attr(755,root,root) %{_bindir}/timed_trigger_test
%endif
%attr(755,root,root) %{_libdir}/libpcl_common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_common.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_features.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_features.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_filters.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_filters.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_geometry.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_geometry.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_io.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_io.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_io_ply.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_io_ply.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_kdtree.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_kdtree.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_keypoints.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_keypoints.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_octree.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_octree.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_registration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_registration.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_sample_consensus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_sample_consensus.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_search.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_search.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_segmentation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_segmentation.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_surface.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_surface.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_tracking.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_tracking.so.1.6
%if %{with vtk}
%attr(755,root,root) %{_libdir}/libpcl_apps.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_apps.so.1.6
%attr(755,root,root) %{_libdir}/libpcl_visualization.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpcl_visualization.so.1.6
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcl_common.so
%attr(755,root,root) %{_libdir}/libpcl_features.so
%attr(755,root,root) %{_libdir}/libpcl_filters.so
%attr(755,root,root) %{_libdir}/libpcl_geometry.so
%attr(755,root,root) %{_libdir}/libpcl_io.so
%attr(755,root,root) %{_libdir}/libpcl_io_ply.so
%attr(755,root,root) %{_libdir}/libpcl_kdtree.so
%attr(755,root,root) %{_libdir}/libpcl_keypoints.so
%attr(755,root,root) %{_libdir}/libpcl_octree.so
%attr(755,root,root) %{_libdir}/libpcl_registration.so
%attr(755,root,root) %{_libdir}/libpcl_sample_consensus.so
%attr(755,root,root) %{_libdir}/libpcl_search.so
%attr(755,root,root) %{_libdir}/libpcl_segmentation.so
%attr(755,root,root) %{_libdir}/libpcl_surface.so
%attr(755,root,root) %{_libdir}/libpcl_tracking.so
%if %{with vtk}
%attr(755,root,root) %{_libdir}/libpcl_apps.so
%attr(755,root,root) %{_libdir}/libpcl_visualization.so
%endif
%{_includedir}/pcl-1.6
%{_pkgconfigdir}/pcl_common-1.6.pc
%{_pkgconfigdir}/pcl_features-1.6.pc
%{_pkgconfigdir}/pcl_filters-1.6.pc
%{_pkgconfigdir}/pcl_geometry-1.6.pc
%{_pkgconfigdir}/pcl_io-1.6.pc
%{_pkgconfigdir}/pcl_kdtree-1.6.pc
%{_pkgconfigdir}/pcl_keypoints-1.6.pc
%{_pkgconfigdir}/pcl_octree-1.6.pc
%{_pkgconfigdir}/pcl_registration-1.6.pc
%{_pkgconfigdir}/pcl_sample_consensus-1.6.pc
%{_pkgconfigdir}/pcl_search-1.6.pc
%{_pkgconfigdir}/pcl_segmentation-1.6.pc
%{_pkgconfigdir}/pcl_surface-1.6.pc
%{_pkgconfigdir}/pcl_tracking-1.6.pc
%if %{with vtk}
%{_pkgconfigdir}/pcl_apps-1.6.pc
%{_pkgconfigdir}/pcl_visualization-1.6.pc
%endif
%dir %{_datadir}/pcl-1.6
%{_datadir}/pcl-1.6/PCLConfig*.cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%dir %{_docdir}/pcl-1.6
%{_docdir}/pcl-1.6/html
%{_docdir}/pcl-1.6/tutorials
%endif
