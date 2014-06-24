{
  'targets': [

    {
      'target_name': 'tree_sitter',
      'type': 'static_library',
      'include_dirs': [
        'include',
        'src',
      ],
      'sources': [
        '<!@(find include src -name "*.h" -or -name "*.cc" -or -name "*.c")',
      ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_RTTI': 'YES',
        'GCC_ENABLE_CPP_EXCEPTIONS': 'NO',
      },
      'direct_dependent_settings': {
        'include_dirs': ['include'],
      },

      # Mac OS has an old version of libstdc++ that doesn't support c++11.
      # libc++ is only present on 10.7 and later.
      'conditions': [
        ['OS == "mac"', {
          'cflags_cc': [ '-stdlib=libc++' ],
          'xcode_settings': {
            'CLANG_CXX_LIBRARY': 'libc++',
            'MACOSX_DEPLOYMENT_TARGET': '10.7',
          },
          'direct_dependent_settings': {
            'cflags_cc': [ '-stdlib=libc++' ],
            'xcode_settings': {
              'CLANG_CXX_LIBRARY': 'libc++',
            },
          },
        }]
      ],
    },

    {
      'target_name': 'compiler_specs',
      'type': 'executable',
      'dependencies': ['tree_sitter'],
      'include_dirs': [
        'src',
        'examples',
        'spec',
        'externals/bandit',
      ],
      'sources': [
        '<!@(find spec/compiler examples/grammars -name "*.h" -or -name "*.cc")',
      ],
    },

    {
      'target_name': 'runtime_specs',
      'type': 'executable',
      'dependencies': ['tree_sitter'],
      'include_dirs': [
        'src',
        'examples',
        'spec',
        'externals/bandit',
      ],
      'variables': {
        'USE_BOOST_REGEX%': 'false',
      },
      'conditions': [
        ['USE_BOOST_REGEX != "false"', {
          'defines': ['USE_BOOST_REGEX'],
          'libraries': ['-lboost_regex'],
        }]
      ],
      'sources': [
        '<!@(find spec/runtime -name "*.h" -or -name "*.cc" -or -name "*.c")',
        '<!@(find examples/parsers -name "*.c")',
        '<!@(find spec/runtime/languages -name "*.txt")',
      ],
    },
  ],

  'target_defaults': {
    'cflags': [
      '-Wall',
      '-Wextra',
      '-Wno-unused-parameter'
    ],
    'cflags_c': [
      '-std=c99'
    ],
    'cflags_cc': [
      '-std=c++0x',
    ],
    'xcode_settings': {
      'CLANG_CXX_LANGUAGE_STANDARD': 'c++11',
      'ALWAYS_SEARCH_USER_PATHS': 'NO',
      'WARNING_CFLAGS': [
        '-Wall',
        '-Wextra',
        '-Wno-unused-parameter'
      ],
    },
  }
}
