# 贡献指南

感谢您对智投项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告Bug

如果您发现了bug，请创建一个Issue并包含以下信息：

- Bug的详细描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、Docker版本等）
- 相关日志或截图

### 提出新功能

如果您有新功能的想法：

1. 先检查是否已有相关Issue
2. 创建新Issue描述功能需求
3. 说明使用场景和预期效果
4. 等待维护者反馈

### 提交代码

1. **Fork项目**
   ```bash
   git clone https://github.com/yourusername/geo-optimizer.git
   cd geo-optimizer
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **开发和测试**
   ```bash
   # 安装依赖
   make install
   
   # 启动开发环境
   make dev
   
   # 运行测试
   make test
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**
   - 在GitHub上创建PR
   - 填写PR模板
   - 等待代码审查

## 代码规范

### Python代码

- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 保持函数简洁（<50行）

```python
def calculate_visibility_score(
    mentions: int,
    total_queries: int,
    position: float
) -> float:
    """
    Calculate visibility score based on mentions and position.
    
    Args:
        mentions: Number of brand mentions
        total_queries: Total number of queries
        position: Average position in results
        
    Returns:
        Visibility score between 0 and 100
    """
    # Implementation
    pass
```

### TypeScript/React代码

- 使用TypeScript严格模式
- 遵循React Hooks最佳实践
- 使用函数组件
- 保持组件简洁（<200行）

```typescript
interface VisibilityCardProps {
  score: number;
  trend: number;
  label: string;
}

export const VisibilityCard: React.FC<VisibilityCardProps> = ({
  score,
  trend,
  label
}) => {
  // Implementation
  return <div>...</div>;
};
```

### 提交信息规范

使用Conventional Commits格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat(research): add multi-language support

- Add language detection
- Support Chinese and English queries
- Update UI for language selection

Closes #123
```

## 测试要求

### 后端测试

```python
import pytest
from app.services.visibility_research import VisibilityResearchService

@pytest.mark.asyncio
async def test_analyze_category():
    service = VisibilityResearchService()
    result = await service.analyze_category("火锅")
    
    assert result["category"] == "火锅"
    assert "maturity" in result
    assert result["maturity"] in ["low", "medium", "high"]
```

### 前端测试

```typescript
import { render, screen } from '@testing-library/react';
import { VisibilityCard } from './VisibilityCard';

test('renders visibility score', () => {
  render(<VisibilityCard score={85} trend={5} label="Overall" />);
  expect(screen.getByText('85%')).toBeInTheDocument();
});
```

## 文档要求

- 更新相关文档（README、API文档等）
- 添加代码注释
- 更新CHANGELOG.md

## 代码审查流程

1. 自动化检查（CI/CD）
2. 代码审查（至少1位维护者）
3. 测试验证
4. 合并到主分支

## 开发环境设置

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

访问: http://localhost:5173

### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

访问: http://localhost:8000/docs

### 数据库迁移

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 获取帮助

- 查看文档: [README.md](README.md)
- 提问: [GitHub Discussions](https://github.com/yourusername/geo-optimizer/discussions)
- 报告问题: [GitHub Issues](https://github.com/yourusername/geo-optimizer/issues)

## 行为准则

- 尊重所有贡献者
- 保持专业和友好
- 接受建设性批评
- 关注项目目标

感谢您的贡献！🎉
