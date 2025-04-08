
# 🛡️ **TorMasker** 🛡️

**TorMasker** is a powerful script designed to frequently change your public IP address using the Tor network. With a simple and automated setup, this tool ensures privacy by rotating IPs every few seconds and logging each IP change along with its location (country and city).

![TorMask](https://github.com/ram-prasad-sahoo/TorMask/blob/main/tool.png)
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

### **Run the Script as Root**:
   The script requires root privileges to perform certain actions. If you're not logged in as root, you’ll need to use `sudo`:

   ```bash
   git clone https://github.com/ram-prasad-sahoo/TorMask.git
   ```
   ```bash
   cd TorMask
   ```
   Create a virtual environment (optional but recommended):
   ```bash
   pip install -r requirements.txt
   ```
   
   ```bash
   sudo python3 tor_masker.py
   ```
---

## 🚨 **Error Handling:**

If you encounter the following error:

```
Error retrieving auth cookie: Could not find a valid Tor authentication cookie at expected paths.
```
![TorMask](https://github.com/ram-prasad-sahoo/TorMask/blob/main/ERROR.png)

**Solution:**

1. Ensure that the Tor service is running. Start or restart Tor using the following commands:
   ```bash
   sudo systemctl start tor
   sudo systemctl restart tor
   ```

---

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


### 🌐 **Setting Up Proxy in Browser**

To ensure that your browser is routed through the Tor network, follow these steps:

1. **Open Your Browser**:
   - Launch the browser you use (e.g., Chrome, Firefox).

2. **Access Browser Settings**:
   - Go to the browser's **Settings** menu.

3. **Search for Proxy Settings**:
   - In the settings search bar, type **"proxy"** or navigate to **Proxy Configuration**.

4. **Enable Manual Proxy Configuration**:
   - In the **Network Settings** or **Connection Settings**, select **Manual Proxy Configuration**.

5. **Set SOCKS Proxy**:
   - In **SOCKS Host**, enter **127.0.0.1** (This is your local IP address).
   - Set the **Port** to **9050** (the default Tor port).

6. **Save Settings**:
   - Once done, click **OK** or **Save** to apply the changes.

---

### 🛠️ **Verify the Connection**

To ensure that the proxy is set up correctly:

1. Open your browser and visit [check.torproject.org](https://check.torproject.org).
2. If the page shows "Congratulations. This browser is configured to use Tor," your connection is set up successfully.
3. Additionally, you can check for any potential DNS leaks to ensure your real IP is hidden.


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

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 🛑 **Important Notes**:

- Ensure that **Tor** is running on your system before using this tool.
- This tool uses the **Tor network**, which is a privacy-focused network. It ensures that your online identity remains anonymous by routing your traffic through multiple nodes in the Tor network.

---

### 🚀 **Enjoy browsing with a new IP!**
