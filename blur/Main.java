import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.color.ColorSpace; 
import java.awt.image.BufferedImage;
import java.awt.image.ColorConvertOp;
import java.io.File;
import java.io.IOException;

public class Main {

    public static double gaussFunc(double x, double y, double a, double b, double sigma) {
        double pi = Math.PI;
        return (1 / (2 * pi * Math.pow(sigma, 2)) * (Math.exp(-(Math.pow((x - a), 2) + Math.pow((y - b), 2)) / (2 * Math.pow(sigma, 2)))));
    }

    public static double[][] buildKernel(int size, double sigma) {
        int a = (size - 1) / 2;
        int b = (size - 1) / 2;
        double[][] kernel = new double[size][size];
        double sum = 0;

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                kernel[i][j] = gaussFunc(i, j, a, b, sigma);
                sum += kernel[i][j];
            }
        }

        // нормализация ядра
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                kernel[i][j] /= sum;
            }
        }
        return kernel;
    }

    public static BufferedImage applyGaussianBlur(BufferedImage image, double[][] kernel) {
        int width = image.getWidth();
        int height = image.getHeight();
        BufferedImage blurredImage = new BufferedImage(width, height, BufferedImage.TYPE_BYTE_GRAY);

        int kernelSize = kernel.length;
        int center = kernelSize / 2;

        for (int i = center; i < height - center; i++) {
            for (int j = center; j < width - center; j++) {
                double red = 0.0;
                double green = 0.0;
                double blue = 0.0;

                for (int m = -center; m <= center; m++) {
                    for (int n = -center; n <= center; n++) {
                        int pixel = image.getRGB(j + n, i + m);
                        double ker = kernel[m + center][n + center];

                        red += ((pixel >> 16) & 0xFF) * ker;
                        green += ((pixel >> 8) & 0xFF) * ker;
                        blue += (pixel & 0xFF) * ker;
                    }
                }
                int blurredColor = ((int) red << 16) | ((int) green << 8) | (int) blue;
                blurredImage.setRGB(j, i, blurredColor);
            }
        }
        return blurredImage;
    }

    public static void main(String[] args) {
        try {
            String imagePath = "C:\\Users\\artus\\PycharmProjects\\MultiMedia\\pictures\\wolf.jpg";
            BufferedImage originalImage = ImageIO.read(new File(imagePath));
            
            ColorConvertOp op = new ColorConvertOp(ColorSpace.getInstance(ColorSpace.CS_GRAY), null);
            originalImage = op.filter(originalImage, null);

            int kernelSize = 5;
            double sigma = 1.0;

            double[][] kernel = buildKernel(kernelSize, sigma);

            BufferedImage blurredImage = applyGaussianBlur(originalImage, kernel);

            JFrame frame = new JFrame();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            JPanel panel = new JPanel();
            panel.setLayout(new GridLayout(1, 2));

            panel.add(new JLabel(new ImageIcon(originalImage)));
            panel.add(new JLabel(new ImageIcon(blurredImage)));

            frame.add(panel);
            frame.pack();
            frame.setVisible(true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
