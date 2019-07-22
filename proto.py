#! python2
# encoding: utf8

import sys
import socket
import test_pb2

def protoTest():
    person = test_pb2.Person()
    person.id = 1234
    person.name ="John Doe"
    person.email ="jdoe@example.com"

    pstr = person.SerializeToString()
    print("pstr", pstr)

# p (CNetClient*)(g_FBServer_Gate.m_mapClients._M_t._M_impl._M_header._M_right)
# boost::details::pool::singleton_default<CFBKernal_Allocator>::instance

# {
#     _M_t = {
#         _M_impl = {
#             <std::allocator<std::_Rb_tree_node<std::pair<unsigned int const, INetService*> > >> = {
#                 <__gnu_cxx::new_allocator<std::_Rb_tree_node<std::pair<unsigned int const, INetService*> > >> = {<No data fields>}, <No data fields>
#             }, 
#             _M_key_compare = {
#                 <std::binary_function<unsigned int, unsigned int, bool>> = {<No data fields>}, <No data fields>
#             },
#             _M_header = {
#                 _M_color = std::_S_red, _M_parent = 0x4efcb250, _M_left = 0x17b80d0, _M_right = 0x4dc00ab8
#             }, 
#             _M_node_count = 667
#        }
#     }
# }
def main():
    protoTest()

main()
