css= '''
<style>
.chat-message {
      padding : 1.5rem; border-radius: 0.5rem, margin-bottom:1rem; display: flex
}
.chat-message.user {
      background-color: #2b313e
}
.chat-message.bot {
      background-color: #475063
}
.chat-message .avatar {
      width: 15%;
}
.chat-message .avatar img {
      max -width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
}
.chat-message .message {
      width: 85%;
      padding: 0 1.5rem;
      color: #fff
}
'''

bot_template='''
<div class="chat-message bot">
  <div class= "avatar">
     <img src=""C:\Users\RupaliPandit\OneDrive - JCW Resourcing\Desktop\AI Chatbot PDFs\download.jpg"" style="max-height: 78px; max-width: 78px; border-radius: 50%">
  </div>
  <div class="message">{{MSG}}</div>
</div>
'''

user_template='''
<div class="chat-message user">
  <div class= "avatar">
     <img src=""C:\Users\RupaliPandit\OneDrive - JCW Resourcing\Desktop\AI Chatbot PDFs\d3c9d91b-2f7f-4207-b41e-5d223e5b36d3.jpg"" >
  </div>
  <div class="message">{{MSG}}</div>
</div>
'''