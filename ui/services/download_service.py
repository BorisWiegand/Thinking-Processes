from pyscript import document, window

class DownloadService:
    
    def download_blob(self, blob, filename: str): 
        data_url = window.URL.createObjectURL(blob)
        self.download_data_url(data_url, filename)
        window.URL.revokeObjectURL(data_url)

    def download_text(self, text: str, filename: str):
        return self.download_blob(
            window.Blob.new(
                [text],
                { "type": "text/plain;charset=utf-8" }
            ),
            filename
        )
    
    def download_data_url(self, data_url, filename: str): 
        anchor_element = document.createElement('a')
        anchor_element.href = data_url
        anchor_element.download = filename

        document.body.appendChild(anchor_element)
        anchor_element.click()

        document.body.removeChild(anchor_element)
        window.URL.revokeObjectURL(anchor_element.href)