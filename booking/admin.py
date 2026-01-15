from django.contrib import admin
from django.utils.html import format_html

from image_cropping import ImageCroppingMixin

from .models import Trip, Seat


@admin.register(Trip)
class TripAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "bus_type",
        "route_from",
        "route_to",
        "depart_at",
        "price",
        "capacity_total",
        "admin_wa",
        "is_active",
        "bus_image_thumb",  # ✅ preview kecil
    )
    list_filter = ("bus_type", "is_active")
    search_fields = ("title", "route_from", "route_to", "admin_wa")

    # Biar form edit lebih enak dipakai
    fieldsets = (
        ("Info Trip", {
            "fields": ("title", "bus_type", "description", "is_active")
        }),
        ("Rute & Jadwal", {
            "fields": ("route_from", "route_to", "depart_at", "price")
        }),
        ("Kapasitas & Admin", {
            "fields": ("capacity_total", "admin_wa")
        }),
        ("Gambar Bus", {
            # bus_image_cropping akan otomatis muncul kalau ada di model
            "fields": ("bus_image", "bus_image_cropping"),
            "description": "Upload gambar bus, lalu atur area crop (free crop).",
        }),
    )

    readonly_fields = ("bus_image_preview",)
    # Tambah preview besar di halaman edit
    def bus_image_preview(self, obj: Trip):
        if getattr(obj, "bus_image", None):
            try:
                return format_html(
                    '<img src="{}" style="max-height:220px;border-radius:12px;object-fit:cover;" />',
                    obj.bus_image.url
                )
            except Exception:
                return "-"
        return "-"

    bus_image_preview.short_description = "Preview"

    # Thumbnail di list display
    def bus_image_thumb(self, obj: Trip):
        if getattr(obj, "bus_image", None):
            try:
                return format_html(
                    '<img src="{}" style="height:42px;width:72px;border-radius:10px;object-fit:cover;" />',
                    obj.bus_image.url
                )
            except Exception:
                return "-"
        return "-"

    bus_image_thumb.short_description = "Bus"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "code",
        "status",
        "hold_until",
        "customer_name",
        "customer_wa",
        "claim_code",
        "booking_code",
        "booked_at",
    )
    list_filter = ("status", "trip")
    search_fields = ("code", "customer_name", "customer_wa", "claim_code", "booking_code")
