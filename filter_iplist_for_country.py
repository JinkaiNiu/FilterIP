import requests
import logging
import os

# 设置日志格式和级别
LOG_FILENAME = "script.log"
logging.basicConfig(
    level=logging.DEBUG,  # 设置最低日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='w', encoding='utf-8'),  # 写入文件
        logging.StreamHandler()  # 控制台输出
    ]
)

def download_file(url, filename, max_retries=3, timeout=10):
    retries = 0
    while retries < max_retries:
        try:
            logging.info(f"开始下载文件: {url}")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # 抛出 HTTP 错误（如 404, 500）
            
            with open(filename, 'wb') as file:
                file.write(response.content)

            logging.info(f"文件下载成功: {filename} (大小: {len(response.content)} 字节)")
            return True
        except requests.exceptions.Timeout:
            logging.warning(f"下载超时，正在重试 ({retries + 1}/{max_retries})...")
        except requests.exceptions.RequestException as e:
            logging.error(f"文件下载失败: {e}")
        
        retries += 1
    
    logging.critical("达到最大重试次数，放弃下载")
    return False

def filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename, country_code='CN'):
    logging.info(f"开始筛选国家代码为 {country_code} 的 IP 地址")
    ipv4_addresses = []
    ipv6_addresses = []

    if not os.path.exists(input_filename):
        logging.error(f"文件未找到: {input_filename}")
        return

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) > 6 and parts[1] == country_code:
                    if parts[2] == 'ipv4':
                        start_ip = parts[3]
                        num_ips = int(parts[4])
                        prefix_length = 32 - num_ips.bit_length()
                        ipv4_addresses.append(f"{start_ip}/{prefix_length}")
                    elif parts[2] == 'ipv6':
                        start_ip = parts[3]
                        prefix_length = parts[4]
                        ipv6_addresses.append(f"{start_ip}/{prefix_length}")

        logging.info(f"共筛选出 {len(ipv4_addresses)} 个 IPv4 地址, {len(ipv6_addresses)} 个 IPv6 地址")

        with open(output_v4_filename, 'w', encoding='utf-8') as file:
            for address in ipv4_addresses:
                file.write(address + '\n')

        with open(output_v6_filename, 'w', encoding='utf-8') as file:
            for address in ipv6_addresses:
                file.write(address + '\n')

        logging.info(f"IPv4 地址已保存到: {output_v4_filename}")
        logging.info(f"IPv6 地址已保存到: {output_v6_filename}")

    except Exception as e:
        logging.error(f"处理文件时发生错误: {e}")

if __name__ == "__main__":
    url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    input_filename = "delegated-apnic-latest"
    output_v4_filename = "all_cn.txt"
    output_v6_filename = "all_cn_ipv6.txt"

    if download_file(url, input_filename):
        filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename)
