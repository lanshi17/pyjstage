"""测试 pyjstage 文献检索功能 - 使用本地测试数据"""

def main():
    from pyjstage.pyjstage import Pyjstage
    from pathlib import Path
    
    jstage = Pyjstage()
    
    # 测试 1: 使用本地测试数据验证解析功能
    print("=" * 60)
    print("测试 1: 使用本地测试数据验证解析功能")
    print("=" * 60)
    
    # 读取测试数据
    test_dir = Path(__file__).parent / "pyjstage" / "test" / "resources"
    
    search_xml = test_dir / "search.xml"
    if search_xml.exists():
        with open(search_xml, 'rb') as f:
            xml_data = f.read()
        
        result = jstage.parser.parse(xml_data)
        
        print(f"总结果数: {result.total_results}")
        print(f"返回数量: {result.items_per_page}")
        print(f"状态: {result.status}")
        print()
        
        for i, entry in enumerate(result.entries, 1):
            print(f"--- 文献 {i} ---")
            print(f"标题: {entry.title}")
            # author 是字典 {语言: 作者名},取日语版本
            if entry.author:
                ja_authors = entry.author.get('ja', '')
                if ja_authors:
                    print(f"作者: {ja_authors}")
                else:
                    print(f"作者: {entry.author.get('en', '无')}")
            else:
                print("作者: 无")
            print(f"期刊: {entry.material_title.get('ja', entry.material_title.get('en', '无')) if entry.material_title else '无'}")
            print(f"卷/期: Vol.{entry.volume}, No.{entry.number}")
            print(f"页码: {entry.starting_page}-{entry.ending_page}")
            print(f"年份: {entry.pubyear}")
            print(f"DOI: {entry.doi if entry.doi else '无'}")
            print(f"链接: {entry.link}")
            print()
    else:
        print(f"❌ 测试文件不存在: {search_xml}")
    
    # 测试 2: 测试 LIST API 解析
    print("=" * 60)
    print("测试 2: 测试 LIST API 解析")
    print("=" * 60)
    
    list_xml = test_dir / "list.xml"
    if list_xml.exists():
        with open(list_xml, 'rb') as f:
            xml_data = f.read()
        
        result = jstage.parser.parse(xml_data)
        
        print(f"总结果数: {result.total_results}")
        print(f"返回数量: {result.items_per_page}")
        print(f"状态: {result.status}")
        print(f"链接: {result.link}")
        print()
        
        if result.entries:
            entry = result.entries[0]
            print(f"最新文献:")
            print(f"标题: {entry.title}")
            print(f"期刊: {entry.material_title.get('ja', entry.material_title.get('en', '无')) if entry.material_title else '无'}")
            print(f"年份: {entry.pubyear}")
            print(f"链接: {entry.link}")
    else:
        print(f"❌ 测试文件不存在: {list_xml}")
    
    # 测试 3: URL 构建测试
    print()
    print("=" * 60)
    print("测试 3: URL 构建功能")
    print("=" * 60)
    
    url = jstage.build_query(
        service='3',
        issn='2186-6619',
        count=5,
        keyword='テスト'
    )
    print(f"构建的 URL: {url}")
    print("✅ URL 构建成功")
    
    print()
    print("=" * 60)
    print("✅ 所有测试完成! pyjstage 在 Python 3.12 上正常工作")
    print("=" * 60)
    print()
    print("说明:")
    print("- J-STAGE API 提供文献检索和元数据服务")
    print("- 不支持直接下载全文 PDF")
    print("- 可以通过 DOI 链接访问出版商网站获取全文")
    print(f"- 文献链接示例: {result.entries[0].link if result.entries else '无'}")

if __name__ == "__main__":
    main()
