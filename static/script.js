document.addEventListener('DOMContentLoaded', function () {
    const slidesDiv = document.getElementById('slides');
    const addSlideBtn = document.getElementById('addSlide');
    const submitBtn = document.getElementById('submit');

    function addSlide() {
        const slideDiv = document.createElement('div');
        slideDiv.className = 'slide';
        slideDiv.innerHTML = `
            <label>Slide Title: <input type="text" class="slide_title"></label><br>
            <label>Slide Text:<br><textarea class="slide_text"></textarea></label><br>
            <label>Image URL: <input type="text" class="image_url"></label>
        `;
        slidesDiv.appendChild(slideDiv);
    }

    addSlideBtn.addEventListener('click', addSlide);
    addSlide();

    submitBtn.addEventListener('click', async () => {
        const title = document.getElementById('title').value;
        const slides = Array.from(document.querySelectorAll('.slide')).map(slide => ({
            slide_title: slide.querySelector('.slide_title').value,
            slide_text: slide.querySelector('.slide_text').value,
            image_url: slide.querySelector('.image_url').value || undefined
        }));
        const response = await fetch('/create_presentation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, slides })
        });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = title + '.pdf';
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert('Failed to create presentation');
        }
    });
});
