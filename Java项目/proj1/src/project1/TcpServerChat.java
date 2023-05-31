package project1;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

import java.sql.ResultSet;

public class TcpServerChat {
    // 客户端发送 -- 用户名+"#"+消息
    // 服务器返回 -- 用户名+"#"+消息+"#"+时间
    // String[] s = recv.split("#"); //s[0]用户名 s[1]消息 s[2]时间
    // 服务器把客户端的消息插入数据库的msg表（用户名，消息，时间）
    // 并把从数据库读取倒数第二条消息作为回应（时间，用户名和消息）

    public ServerMainFrame mainFrame;// 服务器窗口
    SqlCon dataConn;
    ArrayList<String> userList;

    public TcpServerChat() {
        mainFrame = new ServerMainFrame();
        dataConn = SqlCon.getInstance();
        dataConn.connect();
        userList = new ArrayList<String>();
    }

    public void addMsg(String recvStr) {
        mainFrame.appendStr(1, recvStr);
        String[] s = recvStr.split("#");
        String values = String.format("'%s','%s','%s'", s[1], s[2], s[3]);
        try {
            dataConn.executeUpdate("insert into Msg(User_Cde,Msg,WriteTime) values("
                    + values + ")");
        } catch (Exception ex) {

        }
    }

    public String addUser(String[] s) {
        String values = String.format("'%s','%s','%s'", s[1], s[2], s[3]);
        System.out.println("注册" + values);
        if (dataConn.existQuery("select User_Cde from Users where User_Cde='" + s[1] + "'")) {
            return "用户已存在";
        }
        try {
            dataConn.executeUpdate("insert into Users(User_Cde,User_Pass,User_LogTime) values("
                    + values + ")");
        } catch (Exception ex) {
            System.out.println("注册错误");
        }
        userList.add(s[1]);
        mainFrame.showUser(userList);
        return "OK";
    }

    public String login(String[] s) {
        if (!dataConn.existQuery("select User_Cde from Users where User_Cde='" + s[1] + "'")) {
            return "用户不存在";
        }
        if (userList.contains(s[1])) {
            return "用户已登录";
        }
        ResultSet rs = dataConn.executeQuery("select User_Pass from Users where User_Cde='" + s[1] + "'");
        String pass = "no";
        try {
            rs.next();
            pass = rs.getString("User_Pass");
        } catch (Exception ex) {
            System.out.println("登录错误");
        }
        System.out.println("pass=" + pass + "  mypass=" + s[2]);
        if (pass.equals(s[2])) {
            userList.add(s[1]);
            mainFrame.showUser(userList);
            return "OK";
        } else {
            return "密码错误";
        }
    }

    public String getMsg() {
        String s1 = "";
        ResultSet rs = dataConn.executeQuery("select User_Cde,Msg,WriteTime From Msg order by WriteTime");
        try {
            while (rs.next()) {
                // s1 += rs.getString("User_Cde") + "#" + rs.getString("Msg") + "#" +
                // rs.getString("WriteTime");
                s1 += rs.getString("WriteTime") + "  \r" + rs.getString("User_Cde") + ":  \r" + rs.getString("Msg")
                        + "\r\n"; // 加到末尾
            }
        } catch (Exception ex) {

        }
        return s1;
    }

    static String getNow() {
        Calendar cal = Calendar.getInstance();
        SimpleDateFormat sformat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return sformat.format(cal.getTime());
    }

    public static void main(String[] args) throws Exception {
        TcpServerChat server = new TcpServerChat();
        while (server.mainFrame.isUsing && server.mainFrame.isVisible()) {
            ServerSocket serverSocket = new ServerSocket(server.mainFrame.getPort()); // 建立监听套接字
            Socket socket = serverSocket.accept(); // 建立连接套接字. 从请求队列中取客户端的连接请求，没有则阻塞***
            DataInputStream inputFromClient = new DataInputStream(socket.getInputStream());// 建立连接输入字节流
            DataOutputStream outputToClient = new DataOutputStream(socket.getOutputStream());// 建立连接输出字节流
            String s1 = inputFromClient.readUTF(); // 读入UTF-8编码的字符. 从输入缓冲区读入字符，没有则阻塞***

            System.out.println("server get:" + s1);
            String s2 = s1 + "#" + getNow();
            String[] s = s2.split("#");
            if (s[0].equals("0")) {
                // 发送消息
                server.addMsg(s2);
                outputToClient.writeUTF(s2); // 输出UTF-8编码的字符
            } else if (s[0].equals("1")) {
                // 注册
                String result = server.addUser(s);
                outputToClient.writeUTF(result);
            } else if (s[0].equals("2")) {
                // 登录
                String result = server.login(s);
                outputToClient.writeUTF(result);
            } else if (s[0].equals("3")) {
                // 退出
                outputToClient.writeUTF(s2);
                server.userList.remove(s[1]);
                server.mainFrame.showUser(server.userList);
            } else if (s[0].equals("a")) {
                // 获取全部消息记录
                outputToClient.writeUTF(server.getMsg());
            } else {
                outputToClient.writeUTF("error");
            }
            // 关闭连接
            inputFromClient.close();
            outputToClient.close();
            socket.close();
            serverSocket.close();
        }
    }
}
