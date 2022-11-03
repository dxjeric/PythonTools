# 创建VPN目录
mkdir vpn
cd vpn

# 查看linux系统版本
lsb_release -a

# 安装部分软件
apt-get install lrzsz

# 获取一键脚本
wget --no-check-certificate https://raw.githubusercontent.com/quericy/one-key-ikev2-vpn/master/one-key-ikev2.sh

# 执行脚本
bash one-key-ikev2.sh

# 替换账号密码
sed -i "s/myUserName/eric/g" /usr/local/etc/ipsec.secrets
sed -i "s/myUserPass/eric/g" /usr/local/etc/ipsec.secrets

# 启动ipsec
ipsec restart

# 下载配置
sz my_key/ca.cert.pem

# 其他
systemctl status firewalld.service

# strongswan配置 日志
vi /usr/local/etc/strongswan.conf
charon {
        load_modular = yes
        duplicheck {
                enable = no
        }
        compress = yes
        plugins {
                include strongswan.d/charon/*.conf
        }
        dns1 = 8.8.8.8
        dns2 = 8.8.4.4
        nbns1 = 8.8.8.8
        nbns2 = 8.8.4.4
        filelog {
            charon {
                path = /root/charon.log
                time_format = %b %e %T
                ike_name = yes
                append = no
                default = 4
                flush_line = yes
            }
            stderr {
                ike = 3
                knl = 3
            }
        }
}
include strongswan.d/*.conf
