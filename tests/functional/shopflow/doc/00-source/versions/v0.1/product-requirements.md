# ShopFlow — Product Requirements v0.1

**Version:** v0.1
**Date:** 2026-04-30
**Status:** Active

---

## โปรเจ็กต์คืออะไร

ShopFlow คือ e-commerce web app สำหรับร้านค้าขนาดเล็ก
ให้เจ้าของร้านจัดการสินค้า, รับออเดอร์, และดูรายงานยอดขายได้

## ฟีเจอร์หลัก v0.1

1. **Product catalog** — เพิ่ม/แก้/ลบสินค้า, อัปโหลดรูป, ตั้งราคา
2. **Cart & checkout** — ตะกร้าสินค้า + checkout flow
3. **Order management** — ดู/อัปเดตสถานะออเดอร์
4. **Basic reporting** — ยอดขายรายวัน/รายเดือน

## Tech Stack ที่กำหนด

- Next.js 14 (frontend + API routes)
- Supabase (database + auth)
- Vercel (deployment)
- Stripe (payment — phase 2)

## Non-Goals v0.1

- Mobile app (phase 2)
- Multi-store support (phase 3)
- Inventory tracking (phase 2)
