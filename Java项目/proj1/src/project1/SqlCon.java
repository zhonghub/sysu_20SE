package project1;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.sql.SQLException;

public class SqlCon {
    private static SqlCon instance = null;
    private Connection conn;
    private String DRIVER = "com.mysql.cj.jdbc.Driver";
    private String CONN_URL = "jdbc:mysql://localhost:3306/data1";
    private String uName = "root";
    private String uPass = "123456";

    // private final String DRIVER = "com.hxtt.sql.access.AccessDriver";
    // private final String CONN_URL = "jdbc:Access:///./data/msg.mdb"; //
    // .为当前目录，即本项目的根目录。

    // "jdbc:mysql://localhost:3306/data1?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
    // "jdbc:mysql:///./data/data1"; // error

    
    /**
     * @param driver 数据库驱动
     * @param conn_url 数据库连接url
     * @param name 用户名
     * @param pass 密码
     */
    private SqlCon(String driver, String conn_url, String name, String pass) {
        DRIVER = driver;
        CONN_URL = conn_url;
        uName = name;
        uPass = pass;
    }

    private SqlCon() {
    }

    // 单例模型
    public static SqlCon getInstance() {
        if (instance == null) {
            instance = new SqlCon();
        }
        return instance;
    }

    // 建立连接
    boolean connect() {
        try {
            Class.forName(DRIVER);
            conn = DriverManager.getConnection(CONN_URL, uName, uPass);// 连接字符串,用户名，口令
            creatTables();
            return true;
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return false;
    }

    // 创建两个表格
    void creatTables() {
        // insert into Users(User_Cde,User_Pass,User_LogTime)
        // insert into Msg(User_Cde,Msg,WriteTime)
        try {
            ResultSet resultSet = conn.getMetaData().getTables(null, null, "Users", null);
            if (!resultSet.next()) {
                String s1 = "create table Users(User_Cde varchar(20), User_Pass varchar(20), User_LogTime varchar(20))";
                System.out.println(s1);
                creatTable(s1);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            // 处理错误
        }
        try {
            ResultSet resultSet2 = conn.getMetaData().getTables(null, null, "Msg", null);
            if (!resultSet2.next()) {
                String s2 = "create table Msg(User_Cde varchar(20), Msg varchar(20), WriteTime varchar(20))";
                System.out.println(s2);
                creatTable(s2);
            }
        } catch (SQLException e) {
            e.printStackTrace();
            // 处理错误
        }
    }

    /*
     * executeQuery()用于执行查询语句并返回结果集，
     * executeUpdate()用于执行更新操作并返回受影响的行数。
     */

    void creatTable(String sqlSentence) {
        try {
            Statement stat = conn.createStatement(); // 获取执行sql语句的对象
            stat.executeUpdate(sqlSentence); // 执行sql查询，返回结果集
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    // 执行select语句，返回存在结果
    boolean existQuery(String sqlSentence) {
        ResultSet rs = executeQuery(sqlSentence);
        try {
            return (rs != null && rs.next());
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
        return false;
    }

    // 执行SQL查询语句, 返回结果集
    ResultSet executeQuery(String sqlSentence) {
        Statement stat;
        ResultSet rs = null;

        try {
            stat = conn.createStatement(); // 获取执行sql语句的对象
            rs = stat.executeQuery(sqlSentence); // 执行sql查询，返回结果集
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return rs;
    }

    // 执行SQL更新语句,失败返回false，成功则返回true并把影响的记录数保存在cnt中。
    boolean executeUpdate(String sqlSentence) {
        Statement stat;

        int cnt = -1;
        try {
            stat = conn.createStatement(); // 根据连接获取一个执行sql语句的对象
            cnt = stat.executeUpdate(sqlSentence); // 执行sql语句,返回所影响行记录的个数
        } catch (Exception e) {
            // System.out.println(e.getMessage());
        }
        return (cnt >= 0);
    }

    // 显示查询结果（Adapter模式）
    ArrayList<HashMap<String, Object>> getRecords(String querySql, String fields, String types) {
        ArrayList<HashMap<String, Object>> records = new ArrayList<HashMap<String, Object>>();

        ResultSet rs = executeQuery(querySql.replace("{0}", fields));
        String arrFields[] = fields.split(",");

        try {
            while (rs.next()) {
                HashMap<String, Object> hm = new HashMap<String, Object>();
                for (int i = 0; i < arrFields.length; i++) {
                    hm.put(arrFields[i], rs.getObject(arrFields[i]));
                }
                records.add(hm);
                // System.out.println(rs.getString("ID"));
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return records;
    }

}