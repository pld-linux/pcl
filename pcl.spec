# TODO: VTK, MPI, ROS?
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Point Cloud Library - library for point cloud processing
Summary(pl.UTF-8):	Point Cloud Library - biblioteka do operacji na chmurze punktów
Name:		pcl
Version:	1.6.0
Release:	0.1
License:	BSD
Group:		Libraries
#Source0Download: http://pointclouds.org/downloads/
Source0:	http://www.pointclouds.org/assets/files/1.6.0/PCL-%{version}-Source.tar.bz2
# Source0-md5:	f83ca5d0ff290412b0807864b95eba26
Patch0:		%{name}-link.patch
URL:		http://pointclouds.org/
BuildRequires:	OpenNI-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	eigen3 >= 3
BuildRequires:	flann-devel
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	qhull-devel
BuildRequires:	python
BuildRequires:	sed >= 4.0
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

# don't use SSE/SSE2/SSE3 just because compiler and builder host supports it
%{__sed} -i -e '/^PCL_CHECK_FOR_SSE/d' CMakeLists.txt

%build
mkdir build
cd build
%cmake ..
%{__make}

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
%dir %{_datadir}/pcl-1.6
%{_datadir}/pcl-1.6/PCLConfig*.cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%dir %{_docdir}/pcl-1.6
%{_docdir}/pcl-1.6/html
%{_docdir}/pcl-1.6/tutorials
%endif
