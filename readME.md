# 🤖 SPADA Watcher (Anti-Late Bot)

Hey guys! I made this bot so we don't have to keep checking SPADA manually for new assignments. It will scan the site for us and send a notification to our Desktop AND WhatsApp whenever a professor posts something new.

## (Installation)
You need to install a few things first. Open your terminal/cmd and copy-paste this:

```bash
pip install python-dotenv pywhatkit pyautogui selenium plyer
```

## Pengunaan
### Windows

1. Download & Pindah: Download file-nya, bebas mau taruh di Drive C: atau D:.
2. Extract & Terminal: Extract folder-nya, klik kanan di dalam folder terus pilih "Open in Terminal".
3. Install Library: Copy-paste command ini:

```bash
pip install python-dotenv pywhatkit pyautogui selenium plyer
```

5. Setup Akun: Ganti nama .env.example jadi .env. Buka pakai Notepad, terus isi NIM, Password, dan No WA kamu. (Jangan hapus tanda kutipnya ya!)
6. WA Web: Buka WhatsApp Web di browser, pastiin setting "Enter to send" sudah ON.
7. Gas!: Klik 2x file run_bot.bat. Pas dia mulai buka WA otomatis, biarin aja jangan digerakin mouse-nya sampai beres kirim.

### Task scheduler (Windows)

Cari dan buka Task Scheduler di Windows.
Pilih Create Basic Task... di panel kanan.
Kasih nama Bot SPADA terus klik Next.

- Trigger: Pilih When I log on.
- Action: Pilih Start a Program.
- Program/script: Klik Browse, cari dan pilih file run_bot.bat di folder project kamu.

Start in (optional): INI WAJIB DIISI. Copy alamat folder project kamu (misal: D:\PROJECT\BOT SPADA) dan paste di sini (tanpa tanda kutip).

Klik Finish.

Tips Tambahan: Klik kanan task Bot SPADA yang baru dibuat > Properties > tab Conditions > Uncheck "Start the task only if the computer is on AC power" (biar bot tetep jalan meski laptop nggak lagi dicharge)
