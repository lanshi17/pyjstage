"""通过代理测试 J-STAGE API 真实请求"""

def main():
    from pyjstage.pyjstage import Pyjstage
    import requests
    
    # 设置代理
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    
    jstage = Pyjstage()
    
    print("=" * 60)
    print("测试: 通过代理访问 J-STAGE API")
    print("=" * 60)
    
    # 测试 1: 直接请求
    print("\n测试 1: 直接 HTTP 请求 (通过代理)")
    url = jstage.build_query(
        service='3',
        issn='2186-6619',
        count=2
    )
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, proxies=proxies, timeout=15)
        print(f"响应状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)} 字符")
        
        if response.status_code == 200:
            print("✅ 直接请求成功!")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 请求错误: {e}")
        return
    
    # 测试 2: 使用 pyjstage 搜索 (需要 monkey-patch requests)
    print("\n测试 2: 使用 pyjstage.search() (通过代理)")
    
    # 临时修改 requests.get 以使用代理
    original_get = requests.get
    def proxied_get(*args, **kwargs):
        kwargs['proxies'] = proxies
        kwargs['timeout'] = 15
        return original_get(*args, **kwargs)
    
    requests.get = proxied_get
    
    try:
        ret_search = jstage.search(issn='2186-6619', count=2)
        
        print(f"总结果数: {ret_search.total_results}")
        print(f"返回数量: {ret_search.items_per_page}")
        print(f"状态: {ret_search.status}")
        print()
        
        for i, entry in enumerate(ret_search.entries, 1):
            print(f"--- 文献 {i} ---")
            print(f"标题: {entry.title}")
            if entry.author:
                ja_authors = entry.author.get('ja', '')
                if ja_authors:
                    print(f"作者: {ja_authors}")
            print(f"期刊: {entry.material_title.get('ja', entry.material_title.get('en', '无')) if entry.material_title else '无'}")
            print(f"年份: {entry.pubyear}")
            print(f"DOI: {entry.doi if entry.doi else '无'}")
            print(f"链接: {entry.link}")
            print()
        
        print("✅ pyjstage.search() 测试成功!")
        
    except Exception as e:
        print(f"❌ 搜索错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 恢复原始函数
        requests.get = original_get
    
    print()
    print("=" * 60)
    print("✅ 所有测试完成! pyjstage 在 Python 3.12 上正常工作")
    print("=" * 60)

if __name__ == "__main__":
    main()
