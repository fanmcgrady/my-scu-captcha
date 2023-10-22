package org.example;

import com.google.code.kaptcha.impl.DefaultKaptcha;
import com.google.code.kaptcha.util.Config;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

public class Main {
    public static void main(String[] args) throws IOException {
        // 配置Kaptcha参数
        Properties properties = new Properties();
        properties.put("kaptcha.textproducer.char.length", "4"); // 设置验证码长度为4
        properties.put("kaptcha.textproducer.char.string", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"); // 设置所选字符
        properties.put("kaptcha.textproducer.font.size", "40"); // 设置字体大小
        properties.put("kaptcha.textproducer.font.color", "red"); // 设置字体颜色
        properties.put("kaptcha.image.width", "180"); // 设置图片宽度
        properties.put("kaptcha.image.height", "60"); // 设置图片高度
        Config config = new Config(properties);
        DefaultKaptcha kaptchaProducer = new DefaultKaptcha();
        kaptchaProducer.setConfig(config);

        // 生成验证码字符串
        String verificationCode = kaptchaProducer.createText();

        // 根据验证码字符串生成图片
        BufferedImage verificationImage = kaptchaProducer.createImage(verificationCode);

        // 保存图片到文件
        FileOutputStream outputStream = new FileOutputStream(verificationCode + ".png");
        ImageIO.write(verificationImage, "png", outputStream);
    }
}