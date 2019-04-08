# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# def options(opt):
#     pass

# def configure(conf):
#     conf.check_nonfatal(header_name='stdint.h', define_name='HAVE_STDINT_H')

def build(bld):
    module = bld.create_ns3_module('urban-routing', ['core', 'mobility', 'internet'])
    module.source = [
        'model/urban-routing.cc',
        'model/urban-routing-packet.cc',
        'model/urban-routing-packet-queue.cc',
        'model/urban-routing-tag.cc',
        'helper/urban-routing-helper.cc',
        ]

    module_test = bld.create_ns3_module_test_library('urban-routing')
    module_test.source = [
        'test/urban-routing-test-suite.cc',
        ]

    headers = bld(features='ns3header')
    headers.module = 'urban-routing'
    headers.source = [
        'model/urban-routing.h',
        'model/urban-routing-packet.h',
        'model/urban-routing-packet-queue.h',
        'model/urban-routing-tag.h',
        'helper/urban-routing-helper.h',
        ]

#    if bld.env.ENABLE_EXAMPLES:
    bld.recurse('examples')

    # bld.ns3_python_bindings()

