<!-- documents\PSQL_DeployConfigNote.md -->

# 进入一个数据库
一个psql数据库 = 一个 Cluster(集群) = 一个数据目录（PGDATA） + 一个 postmaster 进程
| `psql`客户端在启动时进入任意一个数据库，`psql`通过当前数据库去执行各种操作，包括查询其他数据库`\l`
**通过 PowerShell 进入的命令**
  1. 详细参数：`psql -U postgres -h localhost -p 5432 -d postgres`
    - `-U postgres`：指定用户名。（`postgres` 是默认的超级用户）
    - `-h localhost`：指定服务所在 IP。（默认`localhost`）
    - `-p 5432`：指定服务所在端口。（默认`5432`）
    - `-d postgres`：指定连接进入的服务器。（默认入口服务器`postgres`）
  2. 简略参数：`psql -U postgres`
    - 自动连接 `localhost:5432` 上的 `postgres` 数据库
    - 进入一个 PostgreSQL 数据库后的响应：
      ```
      psql (16.2)
      Type "help" for help.

      postgres=#
      ```
- **语句说明：**
  - `psql (16.2)`：当前使用的是 PostgreSQL 16.2 版本的`psql`客户端
  - `postgres`：当前连接的数据库名
  - `#`：当前是**超级用户**身份
  - `>`：当前是**普通用户**身份
- 当前的工作空间：`postgre`数据库
  - 可输入**SQL语句**或**psql元命令**来操作数据库

- **常用psql元命令：**
  - `\l`：查看**所有数据库**
    - `list`：查看**所有数据库及其详细信息**
  - `\dt`：查看**当前数据库**中的所有表
    - `dt`：desctibe tables
  - `\dv`
  - `\ds`

- **常用SQL语句**
| 每一行SQL语句要求以`;`结尾
  - 创建自己的数据库：`CREATE DATABASE myfastapi_db;`
  - 创建一个专用用户（角色）：`CREATE USER myuser WITH PASSWORD 'mypassword';`
  - 授权：`GRANT ALL PRIVILEGES ON DATABASE myfastapi_db TO myuser;`
  - 退出 psql：`\q`
  - 连接数据库（包括切换）：`\c 数据库名`、`\connect 数据库名`
| 当输入 SQL 语句没有在末尾加`;`时，`psql`会认为在进行多行输入，显示例如`postgres-#`，要安全继续可输入`;`以让 SQL 语句的输入完整结束

## 默认数据库`postgres`
**特性：**
- 默认存在：安装 PostgresSQL 时**自动创建**，**永远存在**
- 轻量&安全：不包含业务数据，适合做操作管理
- 常用语工具连接：`pg_dump`、`pg_restore`、`createdb`等工具默认连接它
**定义：**
- 是 PostgreSQL 的**管理入口数据库**，类似于 Linux 的 `/` 或者 Windows 的 `C:\`
  - 是进入 psql 的默认起点

# 用户
- 一个 PostgreSQL 实例中的用户是跨数据库的，一个 psql 应用中的所有数据库通用。

## 相关命令

## 创建用户
#### SQL
##### 创建普通用户
`CREATE USER 用户名 WITH PASSWORD '密码';`

##### 创建超级用户
`CREATE USER 用户名 WITH SUPERUSER LOGIN PASSWORD '密码'`

##### 创建用户时的权限配置
例如：`CREATE ROLE ccl_dev WITH PASSWORD 'mypassword' LOGIN CREATEDB CREATEROLE;`
- `WITH` 代表后面是定义用户的属性。可以省略。必须在属性配置前面写。
- `PASSWORD '<密码>'` 是定义用户的密码
- `LOGIN` 允许登录
- `CREATEDB` 允许创建数据库
- `CREATEROLE` 允许创建用户
- 各个属性配置的先后顺序可自由调整

### 查询用户
#### SQL
`SELECT current_user;`
或
`SELECT user`
- `user` 是 `current_user` 的别名，psql 特有
- `current_user` 是通用的 SQL 标准函数（无`()`的关键字形态）
- 都是返回当前会话（session）的用户
- 查询“我是谁？”

##### 根据用户权限进行筛选
`SELECT rolname FROM pg_roles WHERE rolsuper = true;`
  - 查询集群中的超级用户

#### psql 元命令
- `\conninfo`
  查询当前连接的详细信息，包括：
    - 用户名
    - 数据库名
    - 主机
    - 端口
- `\du`
  查询当前 psql 实例（PostgreSQL集群（Cluster））所有用户及其属性
  - `du`：describe users
  - `du username` 查询指定用户
  - 实质：`SELECT rolname, rolsuper, rolcreatedb, rolcanlogin, ... FROM pg_roles;`
- `SELECT rolname FROM pg_roles;`
  查询 PostgreSQL 中所有用户（角色）的名称

### 切换用户
切换到其他用户：`SET ROLE myuser;`
切换回原始用户：`RESET ROLE;`、`SET ROLE NONE;`

### 更改用户
#### 撤销用户超级用户权限
`ALTER ROLE 用户名 NOSUPERUSER;`

**注意**
  - 若将集群中所有的超级用户权限都撤销，集群将没有任何超级用户，也没有任何用户可以再创建或赋予超级用户

## `pg_roles`
- 是一个特殊的**系统视图（system view）**，属于 PostgreSQL 的**系统目录（System Catalog）**
- 只读
**作用：**
  - 存储当前 PostgreSQL 实例中所有角色（Role）的信息
| 相当于整个数据库系统的用户列表

## `pg_authid`

# 表操作
## 列
### 查询列
#### psql 元命令
##### `\d+ 表名`
- 详细

##### `\d 表名`
- 简略

#### SQL 语句
##### `pg_catalog` schema
```
SELECT column_name, data_types, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'pg_roles'
  AND table_schema = 'pg_catalog';
```
| `pg_roles`属于`pg_catalog` schema，其他一般默认为`public` 

#### `SELECT * FROM ... LIMIT 1`
- 查询第一条数据的全部列数据，看数据猜结构

# Schema
- 每个数据库包含多个 schema，默认为 `public` schema。
- schema：命名空间。类似于文件夹。
- 系统对象（表、视图、函数等）存放在 `pg_catalog`
- 每个数据库的 schema 独立

| `\dv`、`\dt`等命令默认操作`public`schema，默认查询不到`pg_catalog`schema中的数据
| `\dv` 等价于 `\dv public.*`：只列出 `public` schema 中的视图

## 会话默认 Schema `public`
- psql 的会话配置参数 `search_path` 默认为 `"$user",public`。
  - 含义：首先在以`$user`为名称的`schema`中搜索操作对象，若未找到操作对象则继续在`public``schema`中搜索。

## `pg_catalog` scheme
- 所有数据库都有且内容基本相同

## `schema` 操作
### 查询 schema 下的视图
#### `SELECT COUNT(*) FROM pg_catalog.pg_class WHERE relkind = 'r';`

### 查看 schema 的命令
`\dn`
`\dn+`

### 新建 schema
`CREATE SCHEMA my_schema;`

### 删除 schema
`DROP SCHEMA my_schema CASCADE;`
- `CASCADE` 是对删除模式的设置，默认不指定时为`RESTRICT`

| `DROP` 可删除的目标：`TABLE`、`VIEW`、`FUNCTION`、`SCHEMA`、`DATABASE`、`ROLE`
| - 其中`DATABASE`不支持`CASCADE`模式，必须手动断开连接

#### 删除模式`RESTRICT`和`CASCADE`
- 默认模式：`RESTRICT` 是默认的删除模式，当未指定删除模式时默认为 `RESTRICT` 模式
- 特性：
  - `RESTRICT` 模式下，若删除的数据中有依赖对象（有别处数据依赖于该数据（被引用）），则会报错并取消删除
  - `RESTRICT` 模式下，会先删除所有当前对象及其依赖者（级联删除），然后删除目标本身
- 使用场景
  - 开发、测试：`CASCADE`、`RESTRICT`
  - 生产：`RESTRICT`。生产环境下禁用`CASCADE`，若要删除依赖对象，要自行手动删除。

| `d+` 查看目标的依赖关系
| 删除前备份：`pg_dump -t users mydb > backup.sql`
| Dependents（被依赖者）
| Depends On（依赖项）

# PostgreSQL (Cluster)实例架构
## Diagram：PostgreSQL 的三层对象模型
```
PostgreSQL 实例（Cluster）
|-- pg_authid（全局角色存储）
|-- 全局对象（Cluster-level）（跨所有数据库）
|   |-- 角色（Roles / Users）（存储在 pg_authid）
|   |-- 表空间（Tablespaces）
|   |-- 数据库列表（pg_database）
|   
|-- 数据库（Database）
|   |-- Schema（命名空间，如 public 或 pg_catalog）
|   |   |-- 表（Tables）（元数据在 pg_class）
|   |   |-- 视图（Views）
|   |   |-- 函数（Functions）
|   |   |-- ...
|   |-- Schema（如 my_schema）
|   |   |-- ...
|   |-- 系统 Schema（pg_catalog）（每个数据库都有）
|       |-- 系统表（如 pg_class，pg_namespace）
|       |-- 系统视图（如 pg_roles，pg_tables）
|-- 数据库（Database）
    |-- public
    |--pg_catalog
```

# 关系（Relation）
**Relation** 是以下概念的统称：
  - 表（Table）：普通数据表
  - 视图（View）：虚拟表（用于查询）
  - 物化视图（Materialized View）：物化的视图（存储结果）
  - 序列（Sequence）：自增数字生成器（如主键 ID）
  - 索引（Index）：加速查询的数据结构
  - 外部表（Foreign Table）：指向外部数据源的表

**查询 Relation 的通用命令：**
  **普通查询：** `\d`
  **详细查询：** `\d+`。（含注释、存储参数等等）

**按类型查询 Relation 分类命令：的**
  **Tables：** `\dt`、`\dt+`
  **Views：** `\dv`、`\dv+`
  **Sequences：** `\ds`、`\ds+`
  **Schemas：** `\dn`、`\dn+`（所有者和权限）
  | 查询用户：`\du`，`du+`


# 原子性操作
- 当一个原子性事务中只有一条语句，默认处于 **自动提交模式（autocommit）**，该单条语句被自动包装成一个事务而提交。
- 当一个原子性事务中有多条语句，应当显式使用 **`BEGIN;...COMMIT;`**，
  - 在该事务中，当任何一条语句出错，会进入 **"failed transaction block"**状态，在该状态下 **只可以**显式执行`ROLLBACK`进行整体回滚并推出该状态。
  - 如果在事务出错前执行`SAVEPOINT 保存点名称`设置了保存点（可设置多个），当某条语句出错后 **应用层**必须立即捕获并且在同一事务中执行`ROLLBACK TO 保存点名称`回滚到之前设置的保存点的状态，进行部分地可控的回滚，实现更精细的**原子性**和**一致性**控制（`ROLLBACK`仍然起效，回滚到最开始）。
  - 一旦事务中某语句出错并进入了 **"failed transaction block"**状态，就无法再次使用保存点，只能进行全局`ROLLBACK`

# 导出 Log 到外部文件
## `psql -U postgres -d myfastapi_db -c "\d *.*" > objects.txt`
- 在 psql 外部执行（CMD/PowerShell）