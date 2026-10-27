# Cẩm Nang Tiếng Anh: quy tắc kỹ thuật

Trang tĩnh (GitHub Pages): `index.html` + `data.json` (bản dự phòng) + `hinh/*.svg` (sơ đồ). Dữ liệu gốc ở Google Sheet ID 1EWqyzAMMVO6JkbQL9YcpSJKX34Uf5AQpUlv2E94jFS8; HTML chỉ đọc và hiển thị, sửa nội dung thì sửa ở Sheet rồi cập nhật `data.json`.

## Trước khi giao bất kỳ thay đổi nào
1. Chạy `python3 tools/audit.py 390,768,1366,1905,2560` (cần Playwright). Phải ra `issues: 0`. Không để người dùng tự phát hiện lỗi hiển thị.
2. Xem ảnh chụp ít nhất một trang có sơ đồ ở 390px và ở màn rộng (1905px trở lên).
3. Cập nhật đồng thời Sheet và `data.json` (bản dự phòng phải khớp Sheet).

## Bài học đã trả giá
- **Chữ trong SVG phải có cỡ cố định bằng px.** Chữ SVG không có `font-size` sẽ kế thừa cỡ chữ trang. Cỡ trang tăng theo màn hình thì chữ phình còn ô giữ nguyên nên tràn. Đã đặt `.fig svg{font-size:17px}`; khi vẽ sơ đồ mới phải đo độ vừa của chữ trong ô (audit làm việc này).
- **Bố cục co giãn theo cửa sổ**: lề dùng `clamp(...vw)`, cột dùng `clamp`, cỡ chữ gốc `html{font-size:clamp(16px,.3vw+11px,22px)}`. Phải có trần: khung tối đa 2100px, sơ đồ `.fig` tối đa 1000px, bảng `.tw` tối đa 1400px; nếu không, khi người dùng thu nhỏ trình duyệt (CSS rộng hàng nghìn px) sơ đồ phình khổng lồ còn chữ thì nhỏ.
- **Đừng chỉ nới chiều rộng tối đa** để sửa lề trắng; phải kiểm tra ở cả màn rất rộng và rất hẹp.
- **Bộ nhớ đệm**: `data.json` và `hinh/*` tải với `?v=<phiên bản>` và `cache:"no-cache"`; đổi phiên bản trong `index.html` khi sửa sơ đồ. GitHub Pages giữ `index.html` vài phút, nhắc người dùng bấm Ctrl+Shift+R.
- **Tải Sheet**: dùng `gviz ... &headers=1`; trang kiểm tra cấu trúc dữ liệu Sheet (`okRaw`) và tự chuyển sang `data.json` nếu lệch hoặc lỗi lúc hiển thị. Ô Sheet bắt đầu bằng `+`, `-`, `=` bị hiểu là công thức (`#ERROR!`), dùng `•` thay thế.
- Chữ dài không có khoảng trắng phải cho phép xuống dòng (`overflow-wrap:anywhere` trong `main`); bảng đặt `min-width` cột để không bẻ từng ký tự.
- Sơ đồ mới: dựng bằng script sinh SVG (ví dụ 12 thì), không vẽ tay từng ô, rồi chạy audit.
