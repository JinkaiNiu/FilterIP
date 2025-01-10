import requests

def download_file(url, filename, max_retries=3):
    retries = 0
    while retries < max_retries:
        print("开始下载文件...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"文件下载成功: {filename}")
            return True
        else:
            retries += 1
            print(f"文件下载失败，状态码: {response.status_code}，正在重试({retries}/{max_retries})")
    print("达到最大重试次数，放弃下载")
    return False

def filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename, country_code='CN'):
    print("开始筛选IP地址...")
    ipv4_addresses = []
    ipv6_addresses = []

    try:
        with open(input_filename, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) > 6 and parts[1] == country_code:
                    if parts[2] == 'ipv4':
                        start_ip = parts[3]
                        num_ips = int(parts[4])
                        prefix_length = 32 - (num_ips).bit_length() + 1
                        ipv4_addresses.append(f"{start_ip}/{prefix_length}")
                    elif parts[2] == 'ipv6':
                        start_ip = parts[3]
                        prefix_length = parts[4]
                        ipv6_addresses.append(f"{start_ip}/{prefix_length}")

    except FileNotFoundError:
        print(f"文件未找到: {input_filename}")
        return

    # Write IPv4 addresses to the output file
    with open(output_v4_filename, 'w') as file:
        for address in ipv4_addresses:
            file.write(address + '\n')

    # Write IPv6 addresses to the separate output file
    with open(output_v6_filename, 'w') as file:
        for address in ipv6_addresses:
            file.write(address + '\n')

    print(f"筛选完成，结果已保存到: {output_v4_filename} 和 {output_v6_filename}")

if __name__ == "__main__":
    url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    input_filename = "delegated-apnic-latest"
    output_v4_filename = "all_cn.txt"
    output_v6_filename = "all_cn_ipv6.txt"

    if download_file(url, input_filename):
        filter_ip_addresses_for_country(input_filename, output_v4_filename, output_v6_filename)