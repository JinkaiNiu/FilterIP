import requests
import logging
import os
import time
from datetime import datetime

# 设置日志格式和级别
LOG_FILENAME = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def validate_inputs(url, input_filename, output_v4_filename, output_v6_filename):
    """验证输入参数"""
    if not url.startswith(('http://', 'https://')):
        raise ValueError("无效的URL格式")
    if not all([input_filename, output_v4_filename, output_v6_filename]):
        raise ValueError("文件名不能为空")

def download_file(url, filename, max_retries=3, timeout=10):
    validate_inputs(url, filename, "dummy", "dummy")
    start_time = time.time()
    retries = 0
    
    while retries < max_retries:
        try:
            logging.info(f"第 {retries + 1} 次尝试下载文件: {url}")
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded_size = 0
            
            with open(filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded_size += len(data)
                    if total_size:
                        progress = (downloaded_size / total_size) * 100
                        logging.info(f"下载进度: {progress:.2f}%")

            download_time = time.time() - start_time
            logging.info(f"文件下载成功: {filename}")
            logging.info(f"文件大小: {downloaded_size/1024:.2f} KB")
            logging.info(f"下载用时: {download_time:.2f} 秒")
            return True
            
        except requests.exceptions.Timeout:
            logging.warning(f"下载超时 ({retries + 1}/{max_retries})")
            retries += 1
        except requests.exceptions.RequestException as e:
            logging.error(f"下载错误: {str(e)}")
            retries += 1
        
        if retries < max_retries:
            wait_time = 2 ** retries
            logging.info(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
    
    logging.critical("下载失败，已达到最大重试次数")
    return False

def filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename, country_code='CN'):
    start_time = time.time()
    logging.info(f"开始处理国家代码 {country_code} 的IP地址")
    
    if not os.path.exists(input_filename):
        logging.error(f"输入文件不存在: {input_filename}")
        return False

    ipv4_addresses = []
    ipv6_addresses = []
    total_lines = sum(1 for _ in open(input_filename, 'r', encoding='utf-8'))
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                if i % 10000 == 0:
                    logging.info(f"处理进度: {(i/total_lines)*100:.2f}% ({i}/{total_lines})")
                
                parts = line.strip().split('|')
                if len(parts) > 6 and parts[1] == country_code:
                    if parts[2] == 'ipv4':
                        start_ip = parts[3]
                        num_ips = int(parts[4])
                        prefix_length = 32 - (num_ips - 1).bit_length()
                        ipv4_addresses.append(f"{start_ip}/{prefix_length}")
                    elif parts[2] == 'ipv6':
                        start_ip = parts[3]
                        prefix_length = parts[4]
                        ipv6_addresses.append(f"{start_ip}/{prefix_length}")

        # 保存结果
        for filename, addresses in [(output_v4_filename, ipv4_addresses), 
                                 (output_v6_filename, ipv6_addresses)]:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(addresses))
            logging.info(f"已保存到文件: {filename} (包含 {len(addresses)} 条记录)")

        process_time = time.time() - start_time
        logging.info(f"处理完成! 总用时: {process_time:.2f} 秒")
        logging.info(f"IPv4地址数量: {len(ipv4_addresses)}")
        logging.info(f"IPv6地址数量: {len(ipv6_addresses)}")
        return True

    except Exception as e:
        logging.error(f"处理文件时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        start_time = time.time()
        logging.info("程序开始执行...")
        
        url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
        input_filename = "delegated-apnic-latest"
        output_v4_filename = "all_cn.txt"
        output_v6_filename = "all_cn_ipv6.txt"

        if download_file(url, input_filename):
            if filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename):
                total_time = time.time() - start_time
                logging.info(f"程序成功完成! 总用时: {total_time:.2f} 秒")
            else:
                logging.error("IP地址过滤失败")
        else:
            logging.error("文件下载失败")
            
    except Exception as e:
        logging.critical(f"程序执行出错: {str(e)}")
    finally:
        logging.info("程序执行结束")
