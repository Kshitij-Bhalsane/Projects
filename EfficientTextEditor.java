import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;

public class EfficientTextEditor extends JFrame 
{

    private JTextArea textArea;
    private JFileChooser fileChooser;

    public EfficientTextEditor() 
    {
        setTitle("Efficient Text Editor");
        setSize(600, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        textArea = new JTextArea();
        JScrollPane scrollPane = new JScrollPane(textArea);
        add(scrollPane, BorderLayout.CENTER);

        createMenuBar();

        fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new FileNameExtensionFilter("Text Files", "txt"));

        setLocationRelativeTo(null); // Center the window on the screen
    }

    private void createMenuBar() 
    {
        JMenuBar menuBar = new JMenuBar();
        setJMenuBar(menuBar);

        JMenu fileMenu = new JMenu("File");
        menuBar.add(fileMenu);

        JMenuItem openItem = new JMenuItem("Open");
        openItem.addActionListener(e -> openFile());
        fileMenu.add(openItem);

        JMenuItem saveItem = new JMenuItem("Save");
        saveItem.addActionListener(e -> saveFile());
        fileMenu.add(saveItem);

        JMenuItem exitItem = new JMenuItem("Exit");
        exitItem.addActionListener(e -> System.exit(0));
        fileMenu.add(exitItem);
    }

    private void openFile() 
    {
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) 
        {
            File selectedFile = fileChooser.getSelectedFile();
            try (BufferedReader reader = new BufferedReader(new FileReader(selectedFile))) 
            {
                textArea.setText(""); // Clear existing text
                String line;
                while ((line = reader.readLine()) != null) 
                {
                    textArea.append(line + "\n");
                }
            } 
            catch (IOException e) 
            {
                showError("Error opening file: " + e.getMessage());
            }
        }
    }

    private void saveFile() 
    {
        int returnValue = fileChooser.showSaveDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) 
        {
            File selectedFile = fileChooser.getSelectedFile();
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(selectedFile))) 
            {
                writer.write(textArea.getText());
            } 
            catch (IOException e) 
            {
                showError("Error saving file: " + e.getMessage());
            }
        }
    }

    private void showError(String message) 
    {
        JOptionPane.showMessageDialog(this, message, "Error", JOptionPane.ERROR_MESSAGE);
    }

    public static void main(String[] args) 
    {
        SwingUtilities.invokeLater(() -> {
            EfficientTextEditor editor = new EfficientTextEditor();
            editor.setVisible(true);
        });
    }
}
