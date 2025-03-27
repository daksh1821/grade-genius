import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:my_first_app/login_page.dart'; // Import the LoginPage

class LandingPage extends StatefulWidget {
  const LandingPage({super.key});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {
  bool _isFirstTime = true; // Track if it's the first time

  @override
  void initState() {
    super.initState();
    _checkFirstTimeUser();
  }

  // Function to check if the user has seen the landing page before
  Future<void> _checkFirstTimeUser() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool isFirstTime = prefs.getBool('isFirstTime') ?? true;

    setState(() {
      _isFirstTime = isFirstTime;
    });
  }

  // Function to mark the user as having seen the landing page and navigate to login
  Future<void> _markAsSeen() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isFirstTime', false);

    // Navigate to the LoginPage after marking as seen
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF2E2E2E), // Dark background
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo (Computer with graduation cap)
            Image.asset(
              'assets/images/logo.png', // Replace with your actual image name
              width: 320, // Adjust width
              height: 320, // Adjust height
              fit: BoxFit.contain,
            ),
            const SizedBox(height: 10),
            // "Grade Genius" text with gradient
            ShaderMask(
              shaderCallback: (bounds) => const LinearGradient(
                colors: [Colors.blue, Colors.pink], // Gradient from blue to pink
                begin: Alignment.centerLeft,
                end: Alignment.centerRight,
              ).createShader(bounds),
              child: const Text(
                'Grade Genius',
                style: TextStyle(
                  fontSize: 40,
                  fontWeight: FontWeight.bold,
                  color: Colors.white, // Overridden by gradient
                ),
              ),
            ),
            const SizedBox(height: 20),
            // Subtitle text
            const Text(
              'Smart Teaching Assistant: Reducing Workload\nand Enhancing Feedback',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16, color: Colors.white70),
            ),
            const SizedBox(height: 30),
            // "Get Started" button (Only navigates when clicked)
            ElevatedButton(
              onPressed: () async {
                await _markAsSeen();
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blueAccent, // Button color
                padding: const EdgeInsets.symmetric(
                  horizontal: 30,
                  vertical: 15,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
              child: const Text(
                'Get Started',
                style: TextStyle(fontSize: 18, color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
