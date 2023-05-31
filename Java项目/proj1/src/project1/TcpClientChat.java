package project1;

public class TcpClientChat {
    // 客户端发送 -- num+""#+用户名+"#"+消息
    // num==0普通消息 num==1注册 num==2登录 num==3退出 num==a请求全部消息
    // num==0或3时 服务器返回 -- num+"#"+用户名+"#"+消息+"#"+时间
    // num==a时 服务器返回全部消息
    // num==1或2时 服务器返回注册/登录结果
    // String[] s = recv.split("#"); //s[0]num s[1]用户名 s[2]消息 s[3]时间
    public static void main(String[] args) throws Exception { // throws 出错后把错误处理抛给上层
        new ClientMainFrame();// 客户端主窗口
    }

}
