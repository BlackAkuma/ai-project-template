# ADR-001: ใช้ Next.js 14 เป็น frontend framework

**วันที่:** 2026-04-30
**สถานะ:** Accepted
**ผู้เสนอ:** AI session — 2026-04-30
**Source Reference:** `doc/00-source/versions/v0.1/product-requirements.md` §Tech Stack
**Related Tasks:** T-001

---

## Context

ShopFlow ต้องการ web app ที่ render เร็ว, SEO-friendly, และมี API routes ในตัว
ทีมมี experience กับ React ดี ต้องการ framework ที่ production-ready

## Options ที่พิจารณา

1. **Next.js 14 (App Router)**
   ข้อดี: SSR/SSG built-in, API routes ในตัว, deploy ง่ายบน Vercel, ecosystem ใหญ่
   ข้อเสีย: App Router ยังใหม่ — learning curve สูง

2. **React + Vite + Express**
   ข้อดี: lightweight, flexible
   ข้อเสีย: ต้อง configure เยอะ, SEO ต้องทำเพิ่มเอง

3. **Remix**
   ข้อดี: good data loading patterns
   ข้อเสีย: community เล็กกว่า, ทีมไม่คุ้น

## การตัดสินใจ

เลือก **Next.js 14** เพราะ: ทีมคุ้น React, deploy บน Vercel ง่าย, มี API routes ไม่ต้องตั้ง backend แยก, เหมาะกับ e-commerce ที่ต้องการ SEO

## ผลที่ตามมา

- สิ่งที่ง่ายขึ้น: deploy บน Vercel one-click, SSR สำหรับ product pages
- สิ่งที่ยากขึ้น: App Router mental model ต่างจาก Pages Router
- สิ่งที่ต้องระวัง: Server Components vs Client Components boundary ต้องออกแบบดี

## Review Trigger

ควรทบทวนเมื่อ: Next.js major version break หรือทีมพบ performance bottleneck
