package project1;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.WindowConstants;
import javax.swing.JOptionPane;
import javax.swing.JPasswordField;

public class ClientSubFrame extends JFrame {
    private static final long serialVersionUID = 1L; // 本语句用于序列化，可以不要

    public String host;
    public int port;
    
    private Socket subSocket;

    private JTextField txtField1;
    private JTextField txtField2;
    private JPasswordField password;
    private JFrame jf;

    private String title;
    private String item1;
    private String item2;
    private String defaultStr1;
    private String defaultStr2;

    ClientSubFrame(ClientMainFrame main, int num) {
        host = main.host;
        port = main.port;
        if (num == 1) {
            title = "注册";
            item1 = "用户名:";
            item2 = "密码:";
            defaultStr1 = "";
            defaultStr2 = "";
        } else if (num == 2) {
            title = "登录";
            item1 = "用户名:";
            item2 = "密码:";
            defaultStr1 = "张三";
            defaultStr2 = "123";
        } else {
            title = "设置";
            item1 = "host:";
            item2 = "port:";
            defaultStr1 = host;
            defaultStr2 = "" + port;
        }
        init(main, num);
    }

    /**
     * @param main
     * @param num
     */
    void init(ClientMainFrame main, int num) {

        this.setSize(400, 300); // 设置width和height
        this.setLocationRelativeTo(null); // 居屏幕中间
        this.setLayout(null); // 空布局，可以准确的定位组件在容器中的位置和大小
        this.setTitle(title);
        // this.setTitle("登录");
        jf = this;
        // 注意：JPasswordField用于密码，取值方法String.valueOf(pass.getPassword())
        txtField1 = new JTextField(defaultStr1, 30); // 初值，列数
        JLabel nameLab = new JLabel(item1); //
        nameLab.setBounds(100, 60, 60, 20); // left,top,width,height
        txtField1.setBounds(160, 60, 120, 20);
        this.add(nameLab);
        this.add(txtField1);

        // 注意：JPasswordField用于密码，取值方法String.valueOf(pass.getPassword())
        if (num == 1 || num == 2) {
            password = new JPasswordField(defaultStr2, 30); // 初值，列数
            password.setBounds(160, 100, 120, 20);
            this.add(password);
        } else {
            txtField2 = new JTextField(defaultStr2, 30); // 初值，列数
            txtField2.setBounds(160, 100, 120, 20);
            this.add(txtField2);
        }
        JLabel msgLab = new JLabel(item2); //
        msgLab.setBounds(100, 100, 40, 20); // left,top,width,height
        this.add(msgLab);

        JButton JB1 = new JButton(title);
        JB1.setBounds(160, 160, 100, 30);
        this.add(JB1);
        // 加上按键事件
        ActionListener al = new ActionListener() { 
            @Override
            public void actionPerformed(ActionEvent e) {
                String txt1 = txtField1.getText().trim();
                String txt2;
                // 注意：JPasswordField用于密码，取值方法String.valueOf(pass.getPassword())
                if (num == 1 || num == 2) {
                    txt2 = String.valueOf(password.getPassword());
                } else {
                    txt2 = txtField2.getText().trim();
                    port = Integer.valueOf(txt2);
                    host = txt1;
                    main.setHostPort(host, port);
                    jf.setVisible(false);
                    main.setTitle("客户端: 登录用户:" + main.getUserName() + "  端口:" + main.port + "  host:" + main.host);
                    JOptionPane.showMessageDialog(null, "设置成功！");
                    return;
                }
                if (txt1.isEmpty() || txt2.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "输入不能为空！");
                    return;
                }
                // 发送 -- num+"#"+用户名+"#"+密码
                // num==0普通消息 num==1注册 num==2登录 num==3退出
                String sendStr = num + "#" + txt1 + "#" + txt2;
                // System.out.println("sendStr="+sendStr);
                // 建立连接、发送数据、接收数据、关闭连接。
                try {
                    subSocket = new Socket(host, port); // 与服务器 建立连接。
                    DataInputStream fromServer = new DataInputStream(subSocket.getInputStream());
                    DataOutputStream toServer = new DataOutputStream(subSocket.getOutputStream());
                    toServer.writeUTF(sendStr);// 发送数据
                    String recv = fromServer.readUTF(); // 接收数据
                    System.out.println("send= " + sendStr);
                    System.out.println("recv= " + recv);
                    fromServer.close();
                    toServer.close();
                    subSocket.close();
                    // 接收注册/登录结果
                    if (recv.equals("OK")) {
                        main.isRegister = true;
                        main.setUserName(txt1);
                        main.setTitle("客户端: 登录用户:" + main.getUserName() + "  端口:" + port + "  host:" + host);
                        if (num == 1) {
                            JOptionPane.showMessageDialog(null, "注册成功！");
                        } else if (num == 2) {
                            JOptionPane.showMessageDialog(null, "登录成功！");
                        }
                        jf.setVisible(false);
                        main.readAllMsg();
                        // 这句导致不能同时登录多个用户
                        main.receiveFromServer();
                    } else {
                        JOptionPane.showMessageDialog(null, "失败：" + recv);
                    }
                    // main.socket.close(); // 关闭连接
                } catch (Exception e1) {
                    JOptionPane.showMessageDialog(null, "服务器错误！");
                    //e1.printStackTrace();
                }
            }
        };
        JB1.addActionListener(al);
        this.setVisible(true);
        this.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE);
    }

}
