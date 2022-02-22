# 校验方法
## 格式
{"校验方法": {"检查项": "期望值"}}

## 支持的校验器
| ID |           方法           |             支持的关键字            |                     描述                    |
|:----:|:-----------------------|:---------------------------------|:--------------------------------------------|
| 1  |          equal           |          eq, equal, equals          |                验证元素值等于               |
| 2  |        not_equal         |          ne, neq, not_equal         |               验证元素值不等于              |
| 3  |       greater_than       |           gt, greater_than          |                验证元素值大于               |
| 4  |        less_than         |            lt, less_than            |                验证元素值小于               |
| 5  |    greater_or_equals     |        ge, greater_or_equals        |              验证元素值大于等于             |
| 6  |      less_or_equals      |          le, less_or_equals         |              验证元素值小于等于             |
| 7  |      string_equals       |        str_eq, string_equals        |         验证元素值转换为string后等于        |
| 8  |       length_equal       |         len_eq, length_equal        |              验证元素长度不等于             |
| 9  |   length_greater_than    |     len_gt, length_greater_than     |               验证元素长度大于              |
| 10 | length_greater_or_equals |   len_ge, length_greater_or_equals  |             验证元素长度大于等于            |
| 11 |     length_less_than     |       len_lt, length_less_than      |               验证元素长度小于              |
| 12 |  length_less_or_equals   |    len_le, length_less_or_equals    |             验证元素长度小于等于            |
| 13 |         contains         |          contain, contains          |            验证元素的值中包含xxx            |
| 14 |    contains_if_exist     | contain_if_exist, contains_if_exist | 如果获取到元素不为空，验证元素的值中包含xxx |
| 15 |       contained_by       |        contained_by, in_list        |            验证元素的值包含于xxx            |
| 16 |     not_contained_by     |    not_contained_by, not_in_list    |           验证元素的值不包含于xxx           |
| 17 |         has_key          |               has_key               |         验证字典元素包含key或key列表        |
| 18 |        type_match        |              type_match             |  验证元素的值类型为xxx（python数据类型名）  |
| 19 |       regex_match        |             regex_match             |          验证元素的值匹配正则表达式         |
| 20 |        startswith        |              startswith             |       验证元素的值转字符串后以xxx开头       |
| 21 |         endswith         |               endswith              |       验证元素的值转字符串后以xxx结尾       |


