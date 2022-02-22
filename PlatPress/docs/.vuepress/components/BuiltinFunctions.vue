<template>
  <div class="main">
    <div>
      <p style="padding-left: 10px" v-html="htmlContent" />
    </div>
  </div>
</template>

<script>

export default {
  name: "BuiltinFunctions",
  data() {
    return {
      htmlContent: 'ssssss'
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.htmlContent = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n' +
          '<html><head><title>Python: module functions</title>\n' +
          '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
          '</head><body bgcolor="#f0f0f8">\n' +
          '\n' +
          '<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n' +
          '<tr bgcolor="#7799ee">\n' +
          '<td valign=bottom>&nbsp;<br>\n' +
          '<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong>functions</strong></big></big></font></td\n' +
          '><td align=right valign=bottom\n' +
          '><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:d%3A%5Cworkspace%5Csrc%5Ctest-platform%5Capps%5Capi_test%5Crunner%5Ccore%5Cbuiltin%5Cfunctions.py">d:\\workspace\\src\\test-platform\\apps\\api_test\\runner\\core\\builtin\\functions.py</a></font></td></tr></table>\n' +
          '    <p><tt>@author:TXU<br>\n' +
          '@file:functions.py<br>\n' +
          '@time:2021/10/26<br>\n' +
          '@email:tao.xu2008@outlook.com<br>\n' +
          '@description:&nbsp;预置的函数，测试设计中直接调用</tt></p>\n' +
          '<p>\n' +
          '<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">\n' +
          '<tr bgcolor="#aa55cc">\n' +
          '<td colspan=3 valign=bottom>&nbsp;<br>\n' +
          '<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>\n' +
          '    \n' +
          '<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n' +
          '<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="datetime.html">datetime</a><br>\n' +
          '</td><td width="25%" valign=top><a href="random.html">random</a><br>\n' +
          '</td><td width="25%" valign=top><a href="string.html">string</a><br>\n' +
          '</td><td width="25%" valign=top><a href="time.html">time</a><br>\n' +
          '</td></tr></table></td></tr></table><p>\n' +
          '<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">\n' +
          '<tr bgcolor="#eeaa77">\n' +
          '<td colspan=3 valign=bottom>&nbsp;<br>\n' +
          '<font color="#ffffff" face="helvetica, arial"><big><strong>Functions</strong></big></font></td></tr>\n' +
          '    \n' +
          '<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n' +
          '<td width="100%"><dl><dt><a name="-gen_random_string"><strong>gen_random_string</strong></a>(str_len: int) -&gt; str</dt><dd><tt>生成指定长度的随机字符串<br>\n' +
          ':param&nbsp;str_len:&nbsp;字符串长度<br>\n' +
          ':return:</tt></dd></dl>\n' +
          ' <dl><dt><a name="-get_current_date"><strong>get_current_date</strong></a>(fmt: str = \'%Y-%m-%d\') -&gt; str</dt><dd><tt>获取当前时间，格式自定义，默认：年-月-日<br>\n' +
          ':param&nbsp;fmt:&nbsp;时间格式<br>\n' +
          ':return:</tt></dd></dl>\n' +
          ' <dl><dt><a name="-get_timestamp"><strong>get_timestamp</strong></a>(str_len: int = 13) -&gt; str</dt><dd><tt>获取时间戳，长度&nbsp;0~16<br>\n' +
          ':param&nbsp;str_len:&nbsp;时间戳长度，0~16，默认13<br>\n' +
          ':return:</tt></dd></dl>\n' +
          ' <dl><dt><a name="-sleep"><strong>sleep</strong></a>(n_secs: int)</dt><dd><tt>sleep&nbsp;n&nbsp;秒<br>\n' +
          ':param&nbsp;n_secs:&nbsp;sleep时间，单位：秒<br>\n' +
          ':return:</tt></dd></dl>\n' +
          ' <dl><dt><a name="-uuid4"><strong>uuid4</strong></a>()</dt><dd><tt>0d1072bf-5d0f-4216-bea6-4df9deb8dae9</tt></dd></dl>\n' +
          ' <dl><dt><a name="-uuid4_list"><strong>uuid4_list</strong></a>(n=1)</dt><dd><tt>[\'1727b3fa-1fc4-4849-aeb3-60790624fcbe\']</tt></dd></dl>\n' +
          '</td></tr></table><p>\n' +
          '<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">\n' +
          '<tr bgcolor="#55aa55">\n' +
          '<td colspan=3 valign=bottom>&nbsp;<br>\n' +
          '<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>\n' +
          '    \n' +
          '<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n' +
          '<td width="100%"><strong>faker</strong> = &lt;faker.proxy.Faker object&gt;</td></tr></table>\n' +
          '</body></html>'
    }
  }
}
</script>

<style scoped>

</style>