# 欧洲观察 · Europe Observatory

基于本地10份成功采集的B站字幕制作的中文专题阅读网站。包含10份单篇报告和1份综合对比。

- `reports/`：11份可独立阅读的Markdown报告。
- `data.json`：单篇报告结构化数据。
- `synthesis.json`：综合篇结构化数据。
- `dist/`：GitHub Pages静态站点，可直接托管。
- `build.py`：生成HTML、报告与ZIP，不依赖第三方包。

构建：`python3 build.py`（首次生成首页处理范围需原始index.md）。

本项目不发布原始字幕全文。所有数字为视频口径，未经外部事实核验。报告标注了重合版本、字幕缺失、时间与统计口径问题。
