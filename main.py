import threading
import asyncio
import concurrent.futures
import time

# ==========================================
# 1. ตัวอย่าง Threading (เหมาะกับงานรอ I/O เช่น ดาวน์โหลดไฟล์)
# ==========================================
def io_bound_task_thread(task_id):
    print(f"[Thread] กำลังทำงานที่ {task_id}...")
    time.sleep(2) # จำลองการรอ (หน่วงเวลา 2 วินาที)
    print(f"[Thread] งานที่ {task_id} เสร็จสิ้น!")

def run_threading():
    print("--- เริ่มทดสอบ Threading ---")
    start_time = time.time()
    threads = []
    
    # สร้าง 5 Threads ให้ทำงานพร้อมกัน
    for i in range(1, 6):
        t = threading.Thread(target=io_bound_task_thread, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join() # รอให้ทุก Thread ทำงานเสร็จ
        
    print(f"Threading ใช้เวลาทั้งหมด: {time.time() - start_time:.2f} วินาที\n")

# ==========================================
# 2. ตัวอย่าง Asyncio (เหมาะกับงานรอ I/O ที่มีปริมาณมากๆ ประหยัดทรัพยากร)
# ==========================================
async def io_bound_task_async(task_id):
    print(f"[Asyncio] กำลังทำงานที่ {task_id}...")
    await asyncio.sleep(2) # ใช้ await สลับการทำงานให้ตัวอื่นทำต่อระหว่างรอ
    print(f"[Asyncio] งานที่ {task_id} เสร็จสิ้น!")

async def run_asyncio():
    print("--- เริ่มทดสอบ Asyncio ---")
    start_time = time.time()
    
    # รวบรวมงาน 5 งานให้ทำงานพร้อมกัน
    tasks = [io_bound_task_async(i) for i in range(1, 6)]
    await asyncio.gather(*tasks)
    
    print(f"Asyncio ใช้เวลาทั้งหมด: {time.time() - start_time:.2f} วินาที\n")

# ==========================================
# 3. ตัวอย่าง Process Pool (เหมาะกับงานที่ใช้ CPU คำนวณหนักๆ)
# ==========================================
def cpu_bound_task(task_id):
    print(f"[Process Pool] กำลังคำนวณงานที่ {task_id}...")
    # จำลองการใช้ CPU คำนวณเยอะๆ
    count = 0
    for i in range(10**7): 
        count += 1
    print(f"[Process Pool] งานที่ {task_id} เสร็จสิ้น!")
    return count

def run_process_pool():
    print("--- เริ่มทดสอบ Process Pool ---")
    start_time = time.time()
    
    # กระจายงานไปยัง CPU Cores ต่างๆ
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(cpu_bound_task, range(1, 6))
        
    print(f"Process Pool ใช้เวลาทั้งหมด: {time.time() - start_time:.2f} วินาที\n")

# ==========================================
# ส่วนเรียกใช้งานหลัก
# ==========================================
if __name__ == "__main__":
    # รันทดสอบทีละแบบ
    run_threading()
    
    # รัน asyncio
    asyncio.run(run_asyncio())
    
    # รัน Process Pool (บน Windows ต้องอยู่ใน if __name__ == "__main__" เสมอ)
    run_process_pool()