require('dotenv').config();
const express = require('express');
const cors = require('cors');
const twilio = require('twilio');

const app = express();
app.use(cors());
app.use(express.json());

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhone = process.env.TWILIO_PHONE_NUMBER;
const client = twilio(accountSid, authToken);

// Send OTP
app.post('/send-otp', async (req, res) => {
    const { phoneNumber } = req.body;
    try {
        const otpResponse = await client.verify.v2.services(process.env.TWILIO_SERVICE_SID)
            .verifications.create({ to: phoneNumber, channel: 'sms' });
        res.json({ success: true, message: "OTP Sent!" });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Verify OTP
app.post('/verify-otp', async (req, res) => {
    const { phoneNumber, otp } = req.body;
    try {
        const verificationCheck = await client.verify.v2.services(process.env.TWILIO_SERVICE_SID)
            .verificationChecks.create({ to: phoneNumber, code: otp });
        if (verificationCheck.status === "approved") {
            res.json({ success: true, message: "OTP Verified!" });
        } else {
            res.json({ success: false, message: "Invalid OTP!" });
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(6000, () => console.log("Server running on port 6000"));