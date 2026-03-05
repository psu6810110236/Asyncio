import threading
import asyncio
import concurrent.futures
import time
import urllib.request
import hashlib

# ==========================================
# 1. Threading: เช็คสถานะเว็บไซต์ (Uptime Checker)
# เหมาะกับ I/O Bound: โยน Request ไปพร้อมๆ กันแล้วรอ Server ตอบกลับ
# ==========================================
URLS = ['https://google.com', 'https://github.com', 'https://python.org', 'http://example.com']

def check_url(url):
    try:
        req = urllib.request.urlopen(url, timeout=3)
        print(f"[Threading] 🌐 {url} -> ออนไลน์ (Status: {req.getcode()})")
    except Exception:
        print(f"[Threading] ❌ {url} -> ออฟไลน์/ไม่สามารถเข้าถึงได้")

def run_threading():
    print("--- 1. เริ่มทำงาน Threading (Website Checker) ---")
    start = time.time()
    threads = []
    
    for url in URLS:
        t = threading.Thread(target=check_url, args=(url,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join() # รอให้ทุก Thread ทำงานเสร็จ
        
    print(f"✅ Threading ใช้เวลา: {time.time() - start:.2f} วินาที\n")

# ==========================================
# 2. Asyncio: สแกนพอร์ตเครือข่าย (Port Scanner)
# เหมาะกับ I/O Bound ที่ต้องการ Concurrency สูงๆ (เปิด Connection จำนวนมาก)
# ==========================================
TARGET_HOST = 'example.com'
PORTS_TO_SCAN = [21, 22, 80, 443, 8080]

async def check_port(host, port):
    try:
        # พยายามเชื่อมต่อไปยัง Host และ Port ที่ระบุ
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=1.5)
        print(f"[Asyncio] 🔓 พอร์ต {port} บน {host} -> เปิด (OPEN)")
        writer.close()
        await writer.wait_closed()
    except Exception:
        print(f"[Asyncio] 🔒 พอร์ต {port} บน {host} -> ปิด (CLOSED)")

async def run_asyncio():
    print("--- 2. เริ่มทำงาน Asyncio (Port Scanner) ---")
    start = time.time()
    
    # รวบรวมงานสแกนทุกพอร์ตให้ทำงานพร้อมกัน
    tasks = [check_port(TARGET_HOST, port) for port in PORTS_TO_SCAN]
    await asyncio.gather(*tasks)
    
    print(f"✅ Asyncio ใช้เวลา: {time.time() - start:.2f} วินาที\n")

# ==========================================
# 3. Process Pool: จำลองการแคร็กรหัส / Proof-of-Work
# เหมาะกับ CPU Bound: ใช้ CPU คำนวณรหัส Hash หนักๆ เต็มสปีดทุกคอร์
# ==========================================
def mine_hash(worker_id, difficulty):
    print(f"[Process Pool] 💻 Worker {worker_id} เริ่มคำนวณหา Hash ที่ขึ้นต้นด้วย '0' {difficulty} ตัว...")
    nonce = 0
    prefix = '0' * difficulty
    
    while True:
        # นำ ID และตัวเลข nonce มาต่อกันแล้วเข้ารหัส MD5
        text = f"worker{worker_id}_{nonce}".encode()
        hash_result = hashlib.md5(text).hexdigest()
        
        # ถ้าหา Hash ที่ขึ้นต้นด้วย 00000 เจอ ถือว่าสำเร็จ
        if hash_result.startswith(prefix):
            print(f"[Process Pool] 🎉 Worker {worker_id} สำเร็จ! Nonce: {nonce} -> Hash: {hash_result}")
            return nonce
        nonce += 1

def run_process_pool():
    print("--- 3. เริ่มทำงาน Process Pool (Hash Mining) ---")
    start = time.time()
    
    # แตก Process ไปยัง CPU cores ต่างๆ รัน 4 ตัวพร้อมกัน
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # ตั้งความยากที่ 5 (หา Hash ที่ขึ้นต้นด้วย 00000)
        futures = [executor.submit(mine_hash, i, 5) for i in range(1, 5)]
        
        for future in concurrent.futures.as_completed(futures):
            future.result() # รอผลลัพธ์จากแต่ละ worker
            
    print(f"✅ Process Pool ใช้เวลา: {time.time() - start:.2f} วินาที\n")

# ==========================================
# ส่วนเรียกใช้งานหลัก
# ==========================================
if __name__ == "__main__":
    print("🚀 เริ่มโปรแกรม Network & Security Toolkit...\n")
    
    run_threading()
    asyncio.run(run_asyncio())
    run_process_pool()