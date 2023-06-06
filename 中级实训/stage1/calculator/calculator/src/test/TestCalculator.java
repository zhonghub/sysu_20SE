package test;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.BeforeClass;
import org.junit.AfterClass;
import main.Calculator;

public class TestCalculator {
	private Calculator Calculator = new Calculator();
	private double l;
	private double r;

	public TestCalculator() {
		l = 12;
		r = 4;
	}

	@BeforeClass
	public static void setUpBeforeClass() {
		// System.out.println("begin test\n");
	}

	@AfterClass
	public static void tearDownAfterClass() {
		// System.out.println("\nend test\n");
	}

	// 测试加法函数
	@Test
	public void testAdd() {
		String result = l + r + "";
		assertEquals(result, Calculator.calAdd(l, r));
	}

	// 测试减法函数
	@Test
	public void testSub() {
		String result = l - r + "";
		assertEquals(result, Calculator.calSub(l, r));
	}

	// 测试乘法函数
	@Test
	public void testMul() {
		String result = l * r + "";
		assertEquals(result, Calculator.calMul(l, r));
	}

	// 测试除法函数，除以非0
	@Test
	public void testDev1() {
		String result = l / r + "";
		assertEquals(result, Calculator.calDev(l, r));
	}

	// 测试除法函数，除0
	@Test
	public void testDev2() {
		r = 0;
		String result = "error";
		assertEquals(result, Calculator.calDev(l, r));
	}

}
