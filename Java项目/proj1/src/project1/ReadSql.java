package project1;

import java.io.BufferedReader;
import java.io.FileReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.Types;
import java.sql.ResultSetMetaData;

public class ReadSql {
    // private final String sqlFile = "data/data1.sql";
    private String DRIVER = "com.mysql.cj.jdbc.Driver";
    private String CONN_URL = "jdbc:mysql://localhost:3306/";
    // private final String CONN_URL2 = "jdbc:mysql://localhost:3306/data2";
    private String uName = "root";
    private String uPass = "123456";

    /**
     * @param driver   数据库驱动
     * @param conn_url 数据库连接url
     * @param name     用户名
     * @param pass     密码
     */
    public ReadSql(String driver, String conn_url, String name, String pass) {
        DRIVER = driver;
        CONN_URL = conn_url;
        uName = name;
        uPass = pass;
    }

    public ReadSql() {

    }

    /**
     * @param database1   用于建立连接的数据库
     * @param database2   目标数据库
     * @param sqlFilePath 要加载的目标sql文件
     * 
     * @apiNote 加载sql文件sqlFilePath到目标数据库database2
     */
    public void loadToDatabase(String database1, String database2, String sqlFilePath) {
        try {
            Class.forName(DRIVER);
            Connection connection = DriverManager.getConnection(CONN_URL + database1, uName, uPass);
            Statement statement = connection.createStatement();
            // 如果已经存在叫这个名字的数据库，先删除这个数据库
            String dropTableSql = "DROP DATABASE IF EXISTS " + database2;
            // 创建数据库
            String createDatabaseSql = "CREATE DATABASE " + database2;
            statement.executeUpdate(dropTableSql);
            statement.executeUpdate(createDatabaseSql);
            System.out.println("Database created successfully");
            statement.close();
            connection.close();

            connection = DriverManager.getConnection(CONN_URL + database2, uName, uPass);
            statement = connection.createStatement();

            BufferedReader reader = new BufferedReader(new FileReader(sqlFilePath));
            String line;
            StringBuilder sqlStatements = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                sqlStatements.append(line);

                // 如果您的.sql文件中以分号（;）作为SQL语句的结束符，请执行该语句并清空StringBuilder
                if (line.endsWith(";")) {
                    // System.out.println(sqlStatements.toString());
                    statement.execute(sqlStatements.toString());
                    sqlStatements.setLength(0); // 清空StringBuilder
                }
            }

            reader.close();
            statement.close();
            connection.close();
        } catch (Exception e) {
            e.printStackTrace();
            // 处理错误
        }
    }

    /**
     * @param database    要存储的目标数据库
     * @param sqlFileName 目标文件
     * @apiNote 保存数据库database到sql文件中
     */
    public void saveToFile(String database, String sqlFileName) {
        try {
            Class.forName(DRIVER);
            Connection connection = DriverManager.getConnection(CONN_URL + database, uName, uPass);
            Statement statement = connection.createStatement();
            String exportSql = "SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = '"
                    + database + "'";
            ResultSet resultSet = statement.executeQuery(exportSql);

            StringBuilder sqlStatements = new StringBuilder();
            sqlStatements.append("\nSET NAMES utf8mb4;\n");

            while (resultSet.next()) {
                String tableName = resultSet.getString("table_name");
                String tableSchema = resultSet.getString("table_schema");

                // 获取表的创建语句
                String createTableSql = "SHOW CREATE TABLE " + tableSchema + "." + tableName;
                Statement statement2 = connection.createStatement();
                ResultSet createTableResultSet = statement2.executeQuery(createTableSql);
                if (createTableResultSet.next()) {
                    String createTableStatement = createTableResultSet.getString(2);
                    // sqlStatements.append(
                    // "\n-- ----------------------------\n-- Table structure for " + tableName
                    // + "\n-- ----------------------------\n");
                    sqlStatements.append("DROP TABLE IF EXISTS " + tableName + ";\n");
                    sqlStatements.append(createTableStatement).append(";\n");
                }
                createTableResultSet.close();
                // 获取表的数据
                String selectDataSql = "SELECT * FROM " + tableSchema + "." + tableName;
                ResultSet dataResultSet = statement2.executeQuery(selectDataSql);
                ResultSetMetaData metaData = dataResultSet.getMetaData();
                int columnCount = metaData.getColumnCount();

                // sqlStatements.append(
                // "\n-- ----------------------------\n-- Records of " + tableName
                // + "\n-- ----------------------------\n");
                while (dataResultSet.next()) {
                    StringBuilder insertStatement = new StringBuilder();
                    insertStatement.append("INSERT INTO ").append(tableName).append("(");
                    // 构建插入语句的列名部分
                    for (int i = 1; i <= columnCount; i++) {
                        if (i > 1) {
                            insertStatement.append(", ");
                        }
                        insertStatement.append(metaData.getColumnName(i));
                    }
                    insertStatement.append(") VALUES (");

                    // 构建插入语句的值部分
                    for (int i = 1; i <= columnCount; i++) {
                        if (i > 1) {
                            insertStatement.append(", ");
                        }
                        int columnType = metaData.getColumnType(i);
                        // 根据列的数据类型处理数据
                        if (columnType == Types.INTEGER || columnType == Types.BIGINT) {
                            insertStatement.append(dataResultSet.getLong(i));
                        } else if (columnType == Types.FLOAT || columnType == Types.DOUBLE) {
                            insertStatement.append(dataResultSet.getDouble(i));
                        } else if (columnType == Types.DATE || columnType == Types.TIME
                                || columnType == Types.TIMESTAMP) {
                            insertStatement.append("'").append(dataResultSet.getString(i)).append("'");
                        } else {
                            insertStatement.append("'").append(dataResultSet.getString(i)).append("'");
                        }
                    }

                    insertStatement.append(");");
                    // 将插入语句添加到 sqlStatements
                    sqlStatements.append(insertStatement.toString()).append("\n");
                }
                dataResultSet.close();
            }
            // 将 sqlStatements 写入文件
            Files.write(Paths.get(sqlFileName), sqlStatements.toString().getBytes());
            resultSet.close();
            statement.close();
            connection.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println(sqlFileName+" is saved");
    }

    public static void main(String[] args) {
        ReadSql reader = new ReadSql();
        // reader.loadToDatabase("data1", "data2", "data/data2.sql"); // 少第一行,注释行出错
        reader.saveToFile("data1", "data/data2.sql"); // OK
    }
}
