document.getElementById('saveBtn').addEventListener('click', async () => {
  const status = document.getElementById('status');
  status.innerText = "正在分析内容...";

  // 1. 获取当前标签页信息
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 2. 在网页中执行脚本提取正文（简单示例：提取前1000个字）
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      return {
        title: document.title,
        content: document.body.innerText.substring(0, 1000), // 截取前1k字发给AI
        url: window.location.href
      };
    }
  }, async (results) => {
    const pageData = results[0].result;

    // 3. 发送给你的 Python 后端
    try {
      const response = await fetch('http://localhost:8000/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pageData)
      });
      const data = await response.json();
      status.innerText = `分类：${data.category}\n摘要：${data.summary}`;
    } catch (error) {
      status.innerText = "错误：请确保后端已启动";
    }
  });
});