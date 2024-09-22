from rag_model import retrieve_by_title_similarity
from text_processing import summarize_text

def chatbot_response(question):
    match = retrieve_by_title_similarity(question)
    
    if match == None:
        response = "نأسف أننا ليس لدينا معلومات عن هذا الموضوع. أنا مخصص فقط للإجابة علي الأسئلة المتعلقة بالقضاء والقانون المصري. كيف يمكنني مساعدتك؟"
        return response
    
    summary = summarize_text(match['pdf_text'])
    link = match['sub_link']

    response = f"الموضوع الذي تبحث عنه يتعلق ب {match['sub_title']}\n\n{summary}"
    if link:
        response += f" \n \nيمكنك قراءة المزيد [هنا]({link})"
    
    return response

