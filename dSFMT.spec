%define major	2
%define minor	2
%define mini	3

%define libname		%mklibname %{name} %{major}.%{minor}
%define libname_sse2	%mklibname %{name}-sse2 %{major}.%{minor}
%define devname		%mklibname %{name} -d

Summary:	Double precision SIMD-oriented Fast Mersenne Twister
Name:		dSFMT
Version:	%{major}.%{minor}.%{mini}
Release:	0
Group:		System/Libraries
License:	BSD
Url:		http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/index.html#%{name}
Source0:	http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/SFMT/%{name}-src-%{version}.tar.gz
Patch0:		%{name}-2.2.3-makefile.patch
# The following patches are requied by Julia
#  (julia) https://raw.githubusercontent.com/JuliaLang/julia/master/deps/patches/
Patch100:	dSFMT.h.patch
Patch101:	dSFMT.c.patch

%description
The purpose of dSFMT is to speed up the generation by avoiding the expensive
conversion of integer to double (floating point). dSFMT directly generates
double precision floating point pseudorandom numbers which have the IEEE
Standard for Binary Floating-Point Arithmetic (ANSI/IEEE Std 754-1985)
format. dSFMT is only available on the CPUs which use IEEE 754 format double
precision floating point numbers.

dSFMT doesn't support integer outputs.

dSFMT supports the output of double precision floating point pseudorandom
numbers which distribute in the range of [1, 2), [0, 1), (0, 1] and (0, 1). 
And it also supports the various periods form 2607-1 to 2132049-1.

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library plugin handling
Group:		System/Libraries

%description -n %{libname}
The purpose of dSFMT is to speed up the generation by avoiding the expensive
conversion of integer to double (floating point). dSFMT directly generates
double precision floating point pseudorandom numbers which have the IEEE
Standard for Binary Floating-Point Arithmetic (ANSI/IEEE Std 754-1985)
format. dSFMT is only available on the CPUs which use IEEE 754 format double
precision floating point numbers.

dSFMT doesn't support integer outputs.

dSFMT supports the output of double precision floating point pseudorandom
numbers which distribute in the range of [1, 2), [0, 1), (0, 1] and (0, 1). 
And it also supports the various periods form 2607-1 to 2132049-1.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%doc LICENSE.txt

#---------------------------------------------------------------------------

%package -n %{libname_sse2}
Summary:	Library plugin handling
Group:		System/Libraries

%description -n %{libname_sse2}
The purpose of dSFMT is to speed up the generation by avoiding the expensive
conversion of integer to double (floating point). dSFMT directly generates
double precision floating point pseudorandom numbers which have the IEEE
Standard for Binary Floating-Point Arithmetic (ANSI/IEEE Std 754-1985)
format. dSFMT is only available on the CPUs which use IEEE 754 format double
precision floating point numbers.

dSFMT doesn't support integer outputs.

dSFMT supports the output of double precision floating point pseudorandom
numbers which distribute in the range of [1, 2), [0, 1), (0, 1] and (0, 1). 
And it also supports the various periods form 2607-1 to 2132049-1.

This library is built with SSE2 support enabled.

%files -n %{libname_sse2}
%{_libdir}/lib%{name}-sse2.so.%{major}*
%doc LICENSE.txt

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libname_sse2} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides the header files, link libraries, and documentation for
building applications that use %{name}.

%files -n %{devname}
%doc README.txt README.jp.txt CHANGE-LOG.txt
%{_includedir}/%{name}.h
%{_includedir}/%{name}-common.h
%{_includedir}/%{name}-params.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-sse2.so
%{_libdir}/pkgconfig/%{name}.pc
%doc LICENSE.txt

#---------------------------------------------------------------------------

%prep
%setup -q -n %{name}-src-%{version}
%apply_patches

# pkgconfig
#   standard
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_bindir}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -L\${libdir} -l%{name}
Cflags: -I\${includedir}
EOF
#   sse2
cat > %{name}.sse2.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_bindir}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary} (with sse2 support)
Version: %{version}
Libs: -L\${libdir} -l%{name}  -msse2 -DHAVE_SSE2
Cflags: -I\${includedir}
EOF

# fix file-not-utf8
for f in README.jp.txt
do
  iconv -f iso8859-15 -t utf8 ${f} > ${f}.tmp
  touch -r ${f} ${f}.tmp
  mv -f ${f}.tmp ${f}
done


%build
%setup_compile_flags
%make lib-std lib-sse2

%install
#% makeinstall_std

# libraries
#    standard
install -dm 0755 %{buildroot}%{_libdir}/
install -pm 0755 lib%{name}.so.%{major}.%{minor} %{buildroot}%{_libdir}/
ln -s lib%{name}.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}.so
ln -s lib%{name}.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -s lib%{name}.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}.so.%{major}.%{minor}.%{mini}

#    sse2
install -dm 0755 %{buildroot}%{_libdir}/
install -pm 0755 lib%{name}-sse2.so.%{major}.%{minor} %{buildroot}%{_libdir}/
ln -s lib%{name}-sse2.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}-sse2.so
ln -s lib%{name}-sse2.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}-sse2.so.%{major}
ln -s lib%{name}-sse2.so.%{major}.%{minor} %{buildroot}%{_libdir}/lib%{name}-sse2.so.%{major}.%{minor}.%{mini}
	
# header
install -dm 0755 %{buildroot}%{_includedir}/
install -pm 0644 %{name}.h %{buildroot}%{_includedir}/
install -pm 0644 %{name}-common.h %{buildroot}%{_includedir}/
install -pm 0644 %{name}-params.h %{buildroot}%{_includedir}/

# pkgconfig
install -dm 0755 %{buildroot}%{_libdir}/pkgconfig/
install -pm 0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
%make std-check sse2-check

