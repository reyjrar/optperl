class optperl {

	file { "/opt/perl/lib":
		ensure => directory,
		owner => root, group => vcs_users, mode => 0775
	}

	file { "/usr/local/bin/cpan-checksum":
		owner => root, group => root, mode => 755,
		source => "puppet:///optperl/cpan-checksum"
	}

	define install( $version=516 ) {
		# Variables
		case "$version" {
			514: {
				$perl_version = '5.14.3'
			}
			516: {
				$perl_version = '5.16.2'
			}
		}
		$perl_root = "/opt/perl/${perl_version}"

		package { "opt-perl-$version":
			ensure => installed
		}

		file { "/opt/perl/${perl_version}/lib/${perl_version}/CPAN/Config.pm":
			owner => root, group => root, mode => 644,
			content => template( "optperl/CPAN-Config.pm.erb" ),
			require => Package["opt-perl-$version"]
		}

		file { "/opt/perl/${perl_version}/bin/check_module.pl":
			owner => root, group => root, mode => 755,
			content => template( "optperl/check_module.pl.erb" ),
			require => Package["opt-perl-$version"]
		}

		concat { "${perl_root}/modules.manifest":
			owner => root, group => root, mode =>644,
		}

		tidy { "/root/.cpan-${version}/build":
			age => '2d',
			recurse => true
		}

		file { "/opt/perl/${perl_version}/distroprefs":
			owner => root, group => root, mode => 0644,
			ensure => directory,
			recurse => true,
			force => true,
			purge => true,
			source => "puppet:///optperl/prefs/",
			require => Package["opt-perl-$version"]
		}

		file { "/opt/perl/${perl_version}/distroprefs/prefs-XML-Parser.yml":
			owner => root, group => root, mode => 0644,
			content => template( "optperl/prefs-XML-Parser.yml.erb" ),
			require => File["/opt/perl/${perl_version}/distroprefs/"]
		}
	}

	define module( $version=516 ) {
		# Variables
		case "$version" {
			514: {
				$perl_version = '5.14.3'
			}
			516: {
				$perl_version = '5.16.2'
			}
		}
		$perl_root = "/opt/perl/${perl_version}"

		exec { "optperl-$version-$name":
			environment => [
				"CPAN_HOME=/root/.cpan-${version}",
				"SHELL=/bin/sh",
				"TERM=vt100",
				"USER=root"
			],
			require => [
					File["/opt/perl/${perl_version}/distroprefs/"],
					File["/opt/perl/${perl_version}/lib/${perl_version}/CPAN/Config.pm"],
			],
			command => "${perl_root}/bin/cpan $name",
			unless => "${perl_root}/bin/check_module.pl $name"
		}

		concat::fragment { "perl-$verion-module-$name":
			target => "${perl_root}/modules.manifest",
			content => "${name}\n",
		}
	}
}
