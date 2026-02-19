# 智投 - 快速参考指南

**版本**: 1.0.0  
**状态**: Phase 1 MVP 完成 (100%)  
**更新日期**: 2026年2月11日

---

## 🚀 快速启动

### 启动应用

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端 | http://localhost:5173 | React应用 |
| 后端API | http://localhost:8000 | FastAPI |
| API文档 | http://localhost:8000/docs | Swagger UI |
| RabbitMQ | http://localhost:15672 | guest/guest |
| Neo4j | http://localhost:7474 | neo4j/password |

---

## 📱 应用功能

### 1. Dashboard (100% 完成) ✅
**路由**: `/`

**功能**:
- 整体可见性评分和趋势
- 提及率和引用指标
- 竞争排名显示
- 30天可见性趋势图（Recharts）
- 引擎性能对比图
- 优化推荐列表
- 时间范围选择器（7d/30d/90d）

**核心指标**:
- 整体可见性
- 提及率（Top-3）
- 引用评分（加权）
- 竞争排名

---

### 2. LLM可见性调研 (100% 完成) ✅
**路由**: `/research`

**功能**:
- 类别输入和分析触发
- 实时分析和加载状态
- 成熟度评估（低/中/高）
- Share of Model可视化
- 认知空白识别
- GEO策略推荐
- 后端API集成

**分析输出**:
- 类别成熟度等级
- 品牌份额分布
- 机会识别
- 可执行策略

---

### 3. 实体关系图谱 (100% 完成) ✅
**路由**: `/entity-graph`

**功能**:
- 实体类型统计（品牌、类别、菜系、地点）
- 交互式图谱可视化占位符
- 实体详情列表和连接数
- 类型筛选
- 导出功能
- Neo4j集成就绪

**实体类型**:
- 品牌
- 类别
- 菜系
- 地点

---

### 4. 评测协议 (100% 完成) ✅
**路由**: `/evaluation`

**功能**:
- 协议管理（创建/运行/调度）
- 测试状态跟踪（已完成/运行中/已调度）
- 多引擎测试结果
- 通过/失败/待定指标
- 成功标准配置
- 自动调度
- 结果导出

**测试指标**:
- 各引擎通过率
- 查询覆盖率
- 一致性评分
- 引用准确性

---

### 5. 业务影响分析 (100% 完成) ✅
**路由**: `/business-impact`

**功能**:
- ROI计算和跟踪
- 收入vs投资趋势
- 转化漏斗可视化
- LLM引擎归因
- 关键洞察仪表板
- 基于时间的分析

**指标**:
- 总ROI百分比
- GEO流量收入
- 转化数量和率
- 平均订单价值
- 引擎归因

---

### 6. 集成中心 (100% 完成) ✅
**路由**: `/integrations`

**功能**:
- 已连接集成仪表板
- 可用集成目录
- 类别筛选
- 连接管理
- API文档访问
- Webhook配置

**集成类别**:
- 分析（Google Analytics）
- 电商（Shopify）
- CMS（WordPress）
- CRM（HubSpot）
- 通讯（Slack）
- 自动化（Zapier）

---

### 7. 门店与NAP管理 (100% 完成) ✅
**路由**: `/stores`

**功能**:
- 多地点管理
- NAP一致性跟踪
- 地点验证状态
- 每个地点的LLM可见性
- 批量导入功能
- NAP审计报告

**NAP指标**:
- 整体一致性评分
- 名称准确性
- 地址准确性
- 电话准确性

---

### 8. 地理分析 (100% 完成) ✅
**路由**: `/geo-analysis`

**功能**:
- 区域性能对比
- 语言分布分析
- 本地化机会
- 区域洞察
- 多语言支持跟踪

**区域指标**:
- 按区域的可见性
- 提及和转化
- 语言偏好
- 机会评分

---

### 9. 行业基准 (100% 完成) ✅
**路由**: `/benchmark`

**功能**:
- 行业排名显示
- 性能雷达图
- 竞争格局分析
- 最佳实践跟踪
- 差距分析
- 行业洞察

**基准数据**:
- 行业排名
- 竞争对手对比
- 最佳实践采用
- 性能差距

---

## 🎨 UI组件库

### 玻璃风格组件
- **GlassCard**: 磨砂玻璃效果容器
- **MetricCard**: 带趋势的数据指标显示
- **PageHeader**: 带图标的一致页面头部

### 表单组件
- **Button**: Primary、Secondary、Ghost变体
- **Input**: 带图标支持的文本输入

### 数据可视化
- **VisibilityTrendChart**: 趋势折线图
- **EngineComparisonChart**: 对比柱状图
- **TrendIndicator**: 上升/下降趋势显示

### 布局
- **Sidebar**: 带玻璃效果的导航
- **Header**: 带搜索的顶栏
- **Layout**: 主布局包装器

---

## 🔧 后端API端点

### 调研API
- `POST /api/v1/research/analyze` - 运行类别分析
- `GET /api/v1/research/reports` - 列出所有报告
- `GET /api/v1/research/reports/{id}` - 获取特定报告

### 探针API
- `POST /api/v1/probes/create` - 创建监控探针
- `POST /api/v1/probes/{id}/execute` - 执行探针
- `GET /api/v1/probes/{id}/results` - 获取探针结果
- `GET /api/v1/probes` - 列出所有探针

### 内容API
- `POST /api/v1/content/analyze` - 分析内容质量

### 实验API
- `POST /api/v1/experiments/create` - 创建A/B测试
- `GET /api/v1/experiments/{id}/results` - 获取测试结果
- `GET /api/v1/experiments` - 列出实验

### 优化API
- `POST /api/v1/optimization/recommend` - 获取推荐
- `GET /api/v1/optimization/strategies` - 列出策略

---

## 🗄️ 数据库架构

### PostgreSQL表（7个表）
1. **brands** - 品牌信息
2. **probe_jobs** - 监控任务
3. **probe_data_points** - 探针结果
4. **experiments** - A/B测试
5. **experiment_variants** - 测试变体
6. **visibility_reports** - 调研报告
7. **content_analyses** - 内容评分

### Redis
- 缓存层
- 会话管理
- 实时数据

### Neo4j
- 实体关系
- 知识图谱
- 连接映射

### RabbitMQ
- 任务队列
- 异步处理
- 事件流

---

## 🎯 核心服务

### 1. LLM可见性调研服务
**文件**: `backend/app/services/visibility_research.py`

**组件**:
- QuestionGenerator - 生成测试查询
- BrandExtractor - 提取品牌提及
- Share of Model计算器
- 成熟度评估器
- 空白识别器
- 策略推荐器

### 2. 探针监控服务
**文件**: `backend/app/services/probe_service.py`

**组件**:
- ProbeScheduler - 调度监控
- 探针执行器
- 可见性评分器
- 历史跟踪器

### 3. 内容分析服务
**文件**: `backend/app/services/content_analyzer.py`

**评分维度**:
- 相关性（0-100）
- 权威性（0-100）
- 时效性（0-100）
- 结构（0-100）
- 实体覆盖（0-100）

### 4. LLM适配器
**文件**: `backend/app/services/llm_adapters.py`

**支持的引擎**:
- GPT-4（OpenAI）
- Claude 3（Anthropic）
- Gemini Pro（Google）
- 可扩展更多

---

## 📊 技术栈

### 前端
- React 18 + TypeScript
- TailwindCSS（玻璃风格主题）
- Framer Motion（动画）
- Recharts（数据可视化）
- React Query（数据获取）
- React Router（导航）
- Axios（HTTP客户端）

### 后端
- FastAPI（Python 3.11）
- SQLAlchemy（ORM）
- Pydantic（验证）
- Uvicorn（ASGI服务器）

### 数据库
- PostgreSQL 15
- Redis 7
- Neo4j 5
- RabbitMQ 3

### DevOps
- Docker + Docker Compose
- 健康检查
- 卷持久化
- 网络隔离

---

## 🎨 设计系统

### 配色方案
- **主色**: 深蓝（#3B82F6）
- **强调色**: 青色（#06B6D4）
- **成功**: 绿色（#10B981）
- **警告**: 橙色（#F59E0B）
- **错误**: 红色（#EF4444）
- **中性**: 冷灰（#6B7280）

### 玻璃效果
```css
background: rgba(255, 255, 255, 0.05)
backdrop-filter: blur(12px)
border: 1px solid rgba(255, 255, 255, 0.1)
```

### 排版
- 字体系列: Inter
- 无表情符号（专业B2B风格）
- 图标: Lucide React

---

## 🔐 环境变量

### 必需（在.env中）
```bash
# 数据库
POSTGRES_HOST=postgres
POSTGRES_DB=geo_optimizer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

### 可选（用于真实LLM API）
```bash
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
GOOGLE_API_KEY=your-key
```

---

## 🐛 故障排除

### Docker未运行
**错误**: `unable to get image: error during connect`

**解决方案**:
1. 启动Docker Desktop
2. 等待鲸鱼图标停止动画
3. 运行`docker ps`验证
4. 再次运行`start.bat`

### 端口已被占用
**错误**: `port is already allocated`

**解决方案**:
```bash
docker-compose down
docker-compose up -d
```

### 服务未就绪
**问题**: 前端显示连接错误

**解决方案**:
- 等待30-60秒让所有服务启动
- 检查日志: `docker-compose logs -f backend`
- 验证健康: `docker-compose ps`

---

## 📚 文档文件

- **README.md** - 项目概述
- **INSTALL.md** - 安装指南
- **QUICKSTART.md** - 快速开始指南
- **FEATURES.md** - 功能列表
- **COMPLETION_SUMMARY.md** - 完成状态
- **PROJECT_STATUS.md** - 项目状态
- **QUICK_REFERENCE.md** - 本文件

### 规格文档
- `.kiro/specs/geo-optimizer/requirements.md` - 完整需求
- `.kiro/specs/geo-optimizer/design.md` - 完整设计
- `.kiro/specs/geo-optimizer/tasks.md` - 任务分解

---

## 🎓 开发命令

### Docker命令
```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart backend

# 重建镜像
docker-compose build

# 检查服务状态
docker-compose ps
```

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 后端开发
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 数据库访问
```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres -d geo_optimizer

# Redis
docker-compose exec redis redis-cli

# Neo4j
# 打开浏览器: http://localhost:7474
```

---

## ✅ 项目完成状态

### Phase 1 MVP: 100% 完成 ✅

**后端服务**: 100%
- ✅ LLM可见性调研
- ✅ 探针监控
- ✅ 内容分析
- ✅ LLM适配器
- ✅ 所有API端点

**前端页面**: 100%
- ✅ Dashboard
- ✅ 可见性调研
- ✅ 实体图谱
- ✅ 评测协议
- ✅ 业务影响
- ✅ 集成中心
- ✅ 门店管理
- ✅ 地理分析
- ✅ 行业基准

**基础设施**: 100%
- ✅ Docker设置
- ✅ 数据库架构
- ✅ 一键启动
- ✅ 文档

---

## 🚀 下一步（Phase 2）

### 计划功能
- 真实LLM API集成（需要API密钥）
- 引用提取系统
- 问题集版本化
- 8+个LLM引擎支持
- 高级分析
- 用户认证
- API速率限制

### 时间线
- Phase 2: 6-8周
- Phase 3: 6-8周
- Phase 4: 4-6周
- Phase 5: 2-4周

**总计**: 13个月完成（目标: 2027年4月）

---

**项目状态**: ✅ Phase 1 MVP完成并可使用

**最后更新**: 2026年2月11日
