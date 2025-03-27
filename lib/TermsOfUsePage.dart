import 'package:flutter/material.dart';

class TermsOfUsePage extends StatefulWidget {
  const TermsOfUsePage({super.key});

  @override
  State<TermsOfUsePage> createState() => _TermsOfUsePageState();
}

class _TermsOfUsePageState extends State<TermsOfUsePage> {
  bool showChat = false; // Controls whether to show Terms or Chat UI

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.purple[50],
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Grade Genius',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.purple,
          ),
        ),
      ),
      body: showChat ? _buildChatUI() : _buildTermsUI(),
    );
  }

  /// 📜 Terms of Use UI
  Widget _buildTermsUI() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Center(
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.purple[50],
            borderRadius: BorderRadius.circular(15),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Terms of Use",
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              const Text(
                "By using our AI-powered question-generation tool, you agree to the following terms:",
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 10),
              const Text("• The AI-generated content may not always be accurate or error-free."),
              const Text("• You are solely responsible for reviewing and using the generated questions appropriately."),
              const Text("• We do not take liability for any consequences arising from the use of this AI-generated content."),
              const Text("• You agree to share your data with us for training and personalized content."),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.pop(context), // Go back to Dashboard
                    child: const Text("No", style: TextStyle(color: Colors.purple)),
                  ),
                  const SizedBox(width: 10),
                  TextButton(
                    onPressed: () {
                      setState(() {
                        showChat = true; // Switch to Chat UI
                      });
                    },
                    child: const Text("Yes", style: TextStyle(color: Colors.purple)),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// 💬 Chat UI
  Widget _buildChatUI() {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          color: Colors.purple[800],
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "Grade Genius AI",
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              SizedBox(height: 8),
              Text(
                "A live AI interface that helps you create question papers, discuss student performance, and get solutions—all in real-time.",
                style: TextStyle(fontSize: 14, color: Colors.white),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Align(
                alignment: Alignment.centerRight,
                child: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.blue,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Text(
                    "Hello, I am Raghav!",
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.blue[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Text(
                    "Hi Raghav, I am Grade AI, an AI to help you design question papers, discuss student performance, and get insights.",
                  ),
                ),
              ),
            ],
          ),
        ),
        Container(
          padding: const EdgeInsets.all(8),
          child: Row(
            children: [
              const Expanded(
                child: TextField(
                  decoration: InputDecoration(
                    hintText: "Reply...",
                    border: InputBorder.none,
                  ),
                ),
              ),
              IconButton(icon: const Icon(Icons.attach_file), onPressed: () {}),
              IconButton(icon: const Icon(Icons.send, color: Colors.blue), onPressed: () {}),
            ],
          ),
        ),
      ],
    );
  }
}
