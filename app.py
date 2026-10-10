import asyncio
import flet as ft
from pyrogram import Client

API_ID = 33221794
API_HASH = "00cf30317a32cd1ab0417cc3dd39d352"

app_client = Client("dreclipse_session", api_id=API_ID, api_hash=API_HASH)

def main(page: ft.Page):
    page.title = "Dreclipse - Neural Core"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Bileşenler
    status_text = ft.Text("Durum: Oturum Bekleniyor...", color=ft.colors.AMBER_450, weight=ft.FontWeight.BOLD)
    chat_dropdown = ft.Dropdown(label="Hedef Sohbet / Grup Seçin", width=350, border_color=ft.colors.CYAN_400)
    message_input = ft.TextField(label="Gönderilecek Mesaj / Payload", border_color=ft.colors.CYAN_400, multiline=True)
    delay_input = ft.TextField(label="Gecikme (Saniye / 0 ms için 0 yazın)", value="0", border_color=ft.colors.CYAN_400)
    count_input = ft.TextField(label="Gönderim Adeti (Toplam Paket)", value="1", border_color=ft.colors.CYAN_400)
    log_output = ft.Text("", color=ft.colors.GREEN_400, size=12)

    async def load_chats(e):
        status_text.value = "Durum: Telegram'a bağlanılıyor ve sohbetler taranıyor..."
        page.update()
        try:
            if not app_client.is_connected:
                await app_client.start()
            
            chats = []
            async for dialog in app_client.get_dialogs(limit=40):
                title = dialog.chat.title or dialog.chat.first_name or "Bilinmeyen"
                chats.append(ft.dropdown.Option(key=str(dialog.chat.id), text=f"{title} ({dialog.chat.type.name})"))
            
            chat_dropdown.options = chats
            status_text.value = "Durum: Hazır. Hedef seçebilirsiniz."
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        page.update()

    async def start_sending(e):
        if not chat_dropdown.value:
            log_output.value = "❌ Lütfen bir hedef sohbet seçin!"
            page.update()
            return
        
        target_id = int(chat_dropdown.value)
        text = message_input.value
        try:
            delay = float(delay_input.value)
            count = int(count_input.value)
        except ValueError:
            log_output.value = "❌ Gecikme ve adet sayısal olmalıdır!"
            page.update()
            return

        log_output.value = "🚀 Paket akışı başlatıldı...\n"
        page.update()

        success = 0
        for i in range(1, count + 1):
            try:
                await app_client.send_message(target_id, text)
                success += 1
                log_output.value += f"[{i}/{count}] OK ➔ Gönderildi.\n"
                page.update()
                if delay > 0:
                    await asyncio.sleep(delay)
            except Exception as err:
                log_output.value += f"[{i}/{count}] Hata: {err}\n"
                page.update()

        log_output.value += f"\n🎉 İşlem Tamamlandı! Başarılı: {success}/{count}"
        page.update()

    # Butonlar
    btn_load = ft.ElevatedButton("Sohbetleri Y
