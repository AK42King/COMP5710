# uses the keystone packages
# to ensure that we use the latest precise packages
Exec { logoutput => 'on_failure' }

node 'glance_keystone_mysql' {
  class { '::mysql::server': }
  class { '::keystone':
    debug        => true,
    catalog_type => 'sql',
    admin_token  => Deferred('vault_lookup::lookup', ["SECRET_PATH_75308/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
  }
  class { '::keystone::db::mysql':
    password => Deferred('vault_lookup::lookup', ["SECRET_PATH_35720/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
  }
  class { '::keystone::roles::admin':
    email    => 'test@puppetlabs.com',
    password => Deferred('vault_lookup::lookup', ["SECRET_PATH_49519/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
  }
  class { '::glance::api':
    debug               => true,
    auth_type           => 'keystone',
    keystone_tenant     => 'services',
    keystone_user       => 'glance',
    keystone_password   => Deferred('vault_lookup::lookup', ["SECRET_PATH_89580/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
    database_connection => 'mysql+pymysql://glance:glance@127.0.0.1/glance',
  }
  class { '::glance::backend::file': }

  class { '::glance::db::mysql':
    password => Deferred('vault_lookup::lookup', ["SECRET_PATH_47747/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
    dbname   => 'glance',
    user     => 'glance',
    host     => '127.0.0.1',
    # allowed_hosts = undef,
    # $cluster_id = 'localzone'
  }

  class { '::glance::registry':
    debug               => true,
    auth_type           => 'keystone',
    keystone_tenant     => 'services',
    keystone_user       => 'glance',
    keystone_password   => Deferred('vault_lookup::lookup', ["SECRET_PATH_31032/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
    database_connection => 'mysql+pymysql://glance:glance@127.0.0.1/glance',
  }
  class { '::glance::keystone::auth':
    password => Deferred('vault_lookup::lookup', ["SECRET_PATH_59538/hvs.Str5ggGdums2yaLtYKBiwxPX", 'http://127.0.0.1:8200']),
  }
}

node default {
  fail("could not find a matching node entry for ${clientcert}")
}
