
# 🛡️ **TorMasker** 🛡️

**TorMasker** is a powerful script designed to frequently change your public IP address using the Tor network. With a simple and automated setup, this tool ensures privacy by rotating IPs every few seconds and logging each IP change along with its location (country and city).

---

## 📦 **Features**
- 🌐 **Change Your IP**: Switch to a new IP address from the Tor network regularly.
- 🗺️ **Location Tracking**: Logs the new IP’s location (country & city).
- 📜 **Logging**: Records every IP change in a log file for your reference.
- 🔒 **Privacy Protection**: By using Tor, your online activity is anonymized.

---

## 🔧 **Installation**

Follow the steps below to set up **TorMasker** on your system.

### Prerequisites:
1. **Root Privileges**: The script needs to be run as root.
2. **Required Packages**:
   - `curl`
   - `tor`
   - `jq`
   - `xxd`

---

### 🖥️ **Installation for Different Distros:**

- **Arch/Manjaro/BlackArch**: 
   ```bash
   pacman -S --needed --noconfirm curl tor jq xxd
   ```

- **Debian/Ubuntu/Kali/Parrot**:
   ```bash
   apt update
   apt install -y curl tor jq xxd
   ```

- **Fedora**:
   ```bash
   dnf install -y curl tor jq xxd
   ```

- **openSUSE**:
   ```bash
   zypper install -y curl tor jq xxd
   ```

---

## ⚙️ **Setup**:

### 1. **Run the Script as Root**:
   The script requires root privileges to perform certain actions. If you're not logged in as root, you’ll need to use `sudo`:

   ```bash
   sudo python3 tor_masker.py
   ```

### 2. **Automatic Configuration**:
   The script checks for the required software and makes necessary adjustments to the `torrc` file. It ensures the following Tor settings are applied:
   - **ControlPort 9051**
   - **CookieAuthentication 1**
   - **CookieAuthFileGroupReadable 1**

---

## 🛠️ **Usage**:

After the initial setup, you can use the script to change your IP address. You can also customize the interval between IP changes.

### Steps:
1. **Run the script**.
2. **Input the time interval** (in seconds) to change your IP address.
3. **Watch the magic happen**! 🌟 Your IP will change every few seconds.

---

## 📂 **Logs**:
The script logs every IP change in a file located at:

```
~/Desktop/tor_ip_changed_log.txt
```

The log includes:
- New IP Address 🌐
- Country & City 📍
- Timestamp 🕒

---

## 📜 **License**:

This project is open-source. Feel free to fork and contribute. 💡

---


## 💬 **Support**

If you need help or have any questions, feel free to reach out to me:

- **GitHub Issues**: You can open an issue on the [GitHub Issues page](https://github.com/ram-prasad-sahoo/BYPASS-4XX/issues) for technical support or reporting bugs.
  
- **Email**: You can contact me directly by clicking the button below:

[![Contact via Gmail](https://img.shields.io/badge/Contact%20via-Gmail-c14438?style=flat&logo=gmail&logoColor=white)](mailto:ramprasadsahoo42@gmail.com)

- **LinkedIn**: Connect with me on LinkedIn by clicking the button below:

[![Connect via LinkedIn](https://img.shields.io/badge/Connect%20via-LinkedIn-0077b5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ramprasadsahoo/)

---

I aim to respond as quickly as possible, and your feedback is highly appreciated. Thank you for using **TorMask**!



## 🛑 **Important Notes**:

- Ensure that **Tor** is running on your system before using this tool.
- This tool uses the **Tor network**, which is a privacy-focused network. It ensures that your online identity remains anonymous by routing your traffic through multiple nodes in the Tor network.

---

### 🚀 **Enjoy browsing with a new IP!**
