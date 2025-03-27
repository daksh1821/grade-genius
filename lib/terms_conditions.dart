import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:my_first_app/sign-up_page.dart';

class TermsConditionsPage extends StatefulWidget {
  const TermsConditionsPage({super.key});

  @override
  State<TermsConditionsPage> createState() => _TermsConditionsPageState();
}

class _TermsConditionsPageState extends State<TermsConditionsPage> {
  bool _isChecked = false; // Checkbox state
  Future<void> _saveAcceptance() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setBool('termsAccepted', true); // Save acceptance
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Terms & Conditions",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Terms & Conditions",
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black12,
                      blurRadius: 5,
                      spreadRadius: 1,
                    ),
                  ],
                ),
                child: SingleChildScrollView(
                  child: const Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "1. Introduction",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "Welcome to Grade Genius! By accessing or using this application, you agree to be bound by these terms. If you do not agree with any part of these terms, please do not use the application.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "2. Data Privacy & Security",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "We respect your privacy. We do not sell, trade, or rent users' personal identification information to others. Your data is stored securely and is only accessible by authorized personnel.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "3. User Responsibilities",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "• You must provide accurate and up-to-date information during registration.\n"
                            "• You are responsible for maintaining the confidentiality of your account.\n"
                            "• You must not share login credentials with others.\n"
                            "• Any activity performed using your account is your responsibility.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "4. Prohibited Activities",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "You may not:\n"
                            "• Use the app for illegal activities.\n"
                            "• Attempt to gain unauthorized access to other accounts.\n"
                            "• Modify, distribute, or reverse-engineer any part of the application.\n"
                            "• Violate intellectual property rights related to Grade Genius.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "5. Intellectual Property Rights",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "All content, including text, graphics, logos, and images, remains the property of Grade Genius and is protected under copyright laws. Unauthorized use is strictly prohibited.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "6. Limitation of Liability",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "Grade Genius is not responsible for any direct or indirect damages arising from the use or inability to use our services. The application is provided on an 'as-is' basis, and we make no warranties of any kind.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "7. Termination of Service",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "We reserve the right to terminate or suspend your account if you violate any of these terms. Users may request account deletion at any time via our support team.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "8. Updates to Terms",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "We may update these Terms & Conditions periodically. Continued use of the app after any changes constitutes your acceptance of the new terms.",
                      ),
                      SizedBox(height: 10),

                      Text(
                        "9. Contact Us",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      Text(
                        "If you have any questions regarding these terms, please contact us at support@gradegenius.com.",
                      ),
                      SizedBox(height: 15),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 15),
            Row(
              children: [
                Checkbox(
                  value: _isChecked,
                  onChanged: (value) {
                    setState(() {
                      _isChecked = value!;
                    });
                  },
                  activeColor: Colors.blueAccent,
                ),
                const Expanded(
                  child: Text(
                    "I have read and agree to the Terms & Conditions.",
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isChecked
                    ? () async {
                  await _saveAcceptance();
                  // Navigate back to Sign-Up Page & reload it
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const SignUpPage()),
                  );
                }
                    : null, // Disabled if not checked
                style: ElevatedButton.styleFrom(
                  backgroundColor: _isChecked ? Colors.blueAccent : Colors.grey,
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: const Text(
                  "Accept & Continue",
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
