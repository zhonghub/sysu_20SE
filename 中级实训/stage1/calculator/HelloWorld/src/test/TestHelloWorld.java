package test;

import main.HelloWorld;
import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class TestHelloWorld {
	@Test
	public void test1() {
		// 测试HelloWorld的out()
		String str = "Hello World!";
		// 判断预期结果和实际结果
		assertEquals(str, HelloWorld.out());
	}

}
