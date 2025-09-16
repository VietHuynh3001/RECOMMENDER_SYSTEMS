import streamlit as st
import pandas as pd
import utils as ut
import glob
import warnings

warnings.filterwarnings('ignore')




# CÀI ĐẶT CẤU HÌNH TRANG
st.set_page_config(layout='wide')
# THANH MENU
st.title("RECOMMENDER SYSTEM")
menu = ["Đặt vấn đề", 
        "Phân tích và kết quả", 
        "Hệ thống đề xuất khách sạn 1",
        "Hệ thống đề xuất khách sạn 2",
        "Thông tin từng khách sạn"]
choice = st.sidebar.selectbox('Menu', menu)

list_hotels=ut.list_hotels(34)
# NỘI DUNG PHẦN 'ĐẶT VẤN ĐỀ'
if choice == 'Đặt vấn đề':
    # NỘI DUNG 'VẤN ĐỀ CỦA DOANH NGHIỆP'    
    st.subheader('VẤN ĐỀ CỦA DOANH NGHIỆP')
    text_business_problem=ut.readtxt('RECOMMENDER_BUSINESS_PROBLEM.txt')[0]
    st.write(text_business_problem)
    st.image('https://flyerbonus.bangkokair.com/images/earn-points/lifestyle/agoda/Agoda_Banner_2020.jpg',
              caption='Agoda')
    # NỘI DUNG 'MỤC TIÊU CỦA DỰ ÁN'
    st.subheader('MỤC TIÊU CỦA DỰ ÁN')
    text_objective=ut.readtxt('RECOMMENDER_OBJECTIVE.txt')[0]
    st.write(text_objective)
    st.image('https://www.researchgate.net/publication/323726564/figure/fig5/AS:631605009846299@1527597777415/Content-based-filtering-vs-Collaborative-filtering-Source.png',
              caption='Các phương pháp sử dụng trong dự án')

# NỘI DUNG 'PHÂN TÍCH VÀ KẾT QUẢ'
elif choice == 'Phân tích và kết quả':
    # NỘI DUNG EDA 
    st.subheader("KHAI PHÁ DỮ LIỆU (EDA)")
    text_eda_intro=ut.readtxt('RECOMMENDER_EDA_INTRODUCTION.txt')[0]
    st.write(text_eda_intro)
    # SELECTBOX EDA
    selectbox_eda=['Điểm số','Số đêm','Quốc tịch','Hình thức du lịch','Loại phòng','Mức điểm','Từ khóa']
    choice_eda=st.selectbox(label='EDA',options=selectbox_eda,label_visibility='collapsed')
    index_choice_eda=selectbox_eda.index(choice_eda)
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            # hiển thị các hình ảnh biểu đồ tại đây
            st.image(f"{index_choice_eda}_eda.PNG", width=340, caption=f'Biểu đồ mô tả {choice_eda}')
        with col2:
            # hiển thị nội dung mô tả biểu đồ tại đây
            comment_content=ut.readtxt('RECOMMENDER_EDA_GRAPH_COMMENTS.txt')[1][index_choice_eda].strip()
            st.write(comment_content)

    # NỘI DUNG 'ĐÁNH GIÁ RECOMMENDER SYSTEMS':
    st.subheader("ĐÁNH GIÁ RECOMMENDER SYSTEMS")
    text_eda_intro=ut.readtxt('RECOMMENDER_MODEL_ASSESSMENT.txt')[0]
    st.write(text_eda_intro)
    # SELECTBOX 'ĐÁNH GIÁ RECOMMENDER SYSTEMS':
    selectbox_model=['Collaborative recommender system','Content-based recommender system']
    choice_model=st.selectbox(label='Method',options=selectbox_model,label_visibility='collapsed')
    index_choice_model=selectbox_model.index(choice_model)
    assessment_content=ut.readtxt('RECOMMENDER_MODEL_ASSESSMENT_CONTENT.txt')[1][index_choice_model]
    if choice_model=='Collaborative recommender system':
        with st.container():
            col1,col2=st.columns(2)
            with col1:
                #hiển thị bảng kết quả khi sử dụng 'reviewer_Id' huấn luyện mô hình
                df_userid_assessment=pd.read_csv('regParam_RMSE.csv',delimiter=',')
                st.table(df_userid_assessment)
            with col2:
                # hiển thị nội dung mô tả phần collaborative recommender system
                final_assessment_content=assessment_content.strip().replace('\ufeff','')
                st.write(assessment_content)
            # hiển thị các hình ảnh biểu đồ mô tả kết quả tunning tại đây
            st.image("0_model_assessment.PNG", width=500, caption=f'Biểu đồ mô tả kết quả đánh giá model')
    elif choice_model=='Content-based recommender system':
        with st.container():
            # hiển thị nội dung mô tả phần content-based recommender system
            final_assessment_content=assessment_content.strip().replace('\ufeff','')
            st.write(assessment_content)
            col1,col2=st.columns(2)
            # # hiển thị các hình ảnh biểu đồ mô tả kết quả content-based recommender system tại đây
            with col1:
                st.image('1_model__assessment_gensim.PNG',width=340,caption='Biểu đồ mô tả kết quả đánh giá bằng gensim')
            with col2:
                st.image('1_model_assessment_cosine_similarity.PNG',width=340,caption='Biểu đồ mô tả kết quả đánh giá bằng cosine similarity')
        with st.container():
            col3,col4=st.columns(2)
            with col3:
                st.image('2_model_assessment_gensim_pca.PNG',width=340,caption='Biểu đồ mô tả kết quả đánh giá bằng gensim (PCA)')
            with col4:
                st.image('2_model_assessment_cosine_similarity_pca.PNG',width=340,caption='Biểu đồ mô tả kết quả đánh giá bằng cosine similarity (PCA)')

# NỘI DUNG 'THÔNG TIN HÁCH SẠN':
elif choice == 'Thông tin từng khách sạn':
    st.subheader('LỰA CHỌN KHÁCH SẠN VÀ THÔNG TIN CẦN TRA CỨU')
    hotel_category_introduction=ut.readtxt('RECOMMENDER_HOTEL_CATEGORY_INTRODUCTION.txt')[0]
    st.write(hotel_category_introduction)
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            # Hiển thị danh sách các khách sạn
            hotel_name=st.selectbox(label='##### Khách sạn',options=list_hotels)
        with col2:
            # Hiển thị các hạn mục của khách sạn
            hotel_category=['Thông tin chung',
                            'Thông tin về lượng khách',
                            'Thông tin về loại phòng và hình thức du lịch',
                            'Thông tin về thời gian',
                            'Thông tin về điểm số',
                            'Thông tin về từ khóa']
            hotel_category_choice=st.selectbox(label='##### Thông tin',options=hotel_category)
    # Truy vấn ID khách sạn từ tên khách sạn
    ID=ut.query_hotels_ID(hotel_name)
    # Hiển thị nội dung từng hạng mục khách sạn
    if hotel_category_choice=='Thông tin về từ khóa':
        ut.WordCloud_Hotels(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
    elif hotel_category_choice=='Thông tin chung':
        ut.overall_information(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        name=ut.hotels(ID=ID)[0]
        address=ut.hotels(ID=ID)[1]
        star=ut.hotels(ID=ID)[2]
        description=ut.hotels(ID=ID)[3]
        st.write(f'''
               **Tên khách sạn:** {name}\n
               **Địa chỉ khách sạn:** {address}\n
               **Số sao:** {star}\n''')
    elif hotel_category_choice=='Thông tin về lượng khách':
        ut.vistors_by_nationality(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False) 
    elif hotel_category_choice=='Thông tin về loại phòng và hình thức du lịch':
        ut.GroupName_RoomType(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
    elif hotel_category_choice=='Thông tin về thời gian':
        ut.StayDetails(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
    elif hotel_category_choice=='Thông tin về điểm số':
        ut.Score(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
    

# HIỂN THỊ NỘI DUNG ĐỀ XUẤT KHÁCH SẠN THEO COSINE SIMILARITY
elif choice=='Hệ thống đề xuất khách sạn 1':
    st.subheader('TÌM KIẾM KHÁCH SẠN')
    hotel_recommmendation=ut.readtxt('RECOMMENDER_MODEL_HOTEL_RECOMMENDATION_COSINE_SIM.txt')[0]
    st.write(hotel_recommmendation)
    
    # Tạo điều khiển để người dùng chọn khách sạn
    selected_hotel_name = st.selectbox("##### Chọn khách sạn", list_hotels)
    # Từ khách sạn đã chọn này, người dùng có thể xem thông tin chi tiết của khách sạn
    ID=ut.query_hotels_ID(selected_hotel_name)
    name=ut.hotels(ID=ID)[0]
    address=ut.hotels(ID=ID)[1]
    star=ut.hotels(ID=ID)[2]
    description=ut.hotels(ID=ID)[3]
    st.image('selected_hotel.jpg',width=380)
    st.write(f'''
               **Tên khách sạn:** {name}\n
               **Địa chỉ khách sạn:** {address}\n
               **Số sao:** {star}\n
               **Điểm số:**''')
    ut.overall_information(ID=ID)
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Đề xuất khách sạn dựa vào khách sạn đã tìm kiếm 
    st.subheader('CÓ THỂ BẠN QUAN TÂM')
    df_recommended_hotel=ut.recommmendation_hotel_consine_similarity(ID=ID)
    list_path_rec_hotel_pic=glob.glob('rec_hotel_?.jpg')
    for i,image_path in enumerate(list_path_rec_hotel_pic):
        hotel_name=df_recommended_hotel.iloc[i,2]
        hotel_address=df_recommended_hotel.iloc[i,4]
        hotel_star=df_recommended_hotel.iloc[i,3]
        hotel_score=df_recommended_hotel.iloc[i,5]
        with st.expander(label=f'#### {hotel_name}',expanded=True):
            image_col,text_col=st.columns(2)
            with image_col:
                st.image(image_path,width=400)
            with text_col:
                st.write(f'''
                        **Địa chỉ khách sạn:** {hotel_address}\n
                        **Số sao:** {hotel_star}\n
                        **Điểm số tổng:** {hotel_score}''')



# HIỂN THỊ NỘI DUNG ĐỀ XUẤT KHÁCH SẠN THEO ALS
elif choice=='Hệ thống đề xuất khách sạn 2':
    # ĐỌC FILE KẾT QUẢ GỢI Ý CỦA ALS
    df_recommended_hotel_als=pd.read_csv('DATA_RECOMMENDATION_UI.csv')
    # DANH SÁCH TÊN CÁC REVIEWERS
    list_name_reviewer=df_recommended_hotel_als['Reviewer Name'].unique()
    name=st.selectbox(label='##### Tên đăng nhập',
                      options=list_name_reviewer)
    # DANH SÁCH TÊN CÁC QUỐC GIA ỨNG VỚI REVIEWERS ĐÃ CHỌN
    list_respectivve_nationality=df_recommended_hotel_als[df_recommended_hotel_als['Reviewer Name']==name]['Nationality'].unique()
    nationality=st.selectbox(label='##### Quốc tịch',
                             options=list_respectivve_nationality)
    password=st.text_input(label='##### Mật khẩu',
                           type='password',placeholder='Mật khẩu là 1234')
    button=st.button('Đăng nhập')
    if name and nationality and password=='1234' and button:
        st.success('Bạn đã đăng nhập thành công')
        image_section,text_section=st.columns(2)
        with text_section:
            st.write(f'**Tên của bạn:** {name}')
            st.write(f'**Quốc tịch:** {nationality}')
        with image_section:
            st.image('avata.jpg',caption='Ảnh đại diện',width=600)
        st.subheader('CÓ THỂ BẠN QUAN TÂM')
        df_recommended_hotel=ut.Collaborative_filtering_recommender_system(name,nationality)
        list_path_rec_hotel_pic=glob.glob('rec_hotel_?.jpg')
        for i,image_path in enumerate(list_path_rec_hotel_pic[:6]):
            hotel_name=df_recommended_hotel.iloc[i,2]
            hotel_id=ut.query_hotels_ID(hotel_name)
            hotel_address=ut.hotels(hotel_id)[1]
            hotel_star=ut.hotels(hotel_id)[2]
            with st.expander(label=f'#### {hotel_name}',expanded=True):
                image_col,text_col=st.columns(2)
                with image_col:
                    st.image(image_path,width=400)
                with text_col:
                    st.write(f'''
                        **Địa chỉ khách sạn:** {hotel_address}\n
                        **Số sao:** {hotel_star}\n''')

    elif button:
        st.error('Xin hãy đăng nhập lại')
    else:

        pass  