import streamlit as st
import utils as ut
import pandas as pd
import glob
import warnings
warnings.filterwarnings('ignore')

# CÀI ĐẶT CẤU HÌNH TRANG
st.set_page_config(layout='wide',
                   page_title='Trang web chính thức của Hotels',
                   page_icon='hotel.png')

#TRANG TRÍ WEB
st.markdown("""
    <style>
    /* Ẩn logo streamlit*/
    footer {
        visibility: hidden;
    }
    header.css-18ni7ap.e13qjvis2 {
        visibility: hidden;
    }
    /* Toàn bộ background */
    .stApp {
        background-image: url('https://i.pinimg.com/originals/59/c2/70/59c270f7d10071f06fc4e2b233f77267.gif');
        background-attachment: fixed;
        background-size: 700px 700px;
        backkground-position: center bottom;
        font-family: 'Arial', sans-serif;
    }
    /* Thanh menu */
    .menu {
        background-color: #003366;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .menu button {
        background-color: #ffcc00 !important;
        color: #003366 !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 8px 16px;
        border: none;
    }
    /* Tiêu đề slogan */
    .slogan {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #003366;
        margin-bottom: 30px;
    }
    /* Ô selectbox */
    div[data-baseweb="select"] {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #003366;
        cursor: pointer !important;
        margin-top: 0px !important;
    }
    /*Form đăng nhập và đăng ký*/
    div.css-12ttj6m.en8akda1 {
        background-color: lightblue !important;
        border-radius: 35px !important;
        border-color: navy !important;
    }
    /*Khung đề xuất khách sạn*/
    .css-1fcdlhc.e1mp27150 {
        background-color: lightskyblue;
        border-radius: 30px; 
       
    }
    .streamlit-expander {
        border-radius: 30px !important;
        border-width:2px;
        border-color: #0000CD;
        overflow: hidden;
    }
    .streamlit-expanderContent {
        border-radius: 30px !important;
    }
    /*Nút bấm trên thanh menu*/
    .stButton > button {
        border: none !important;
        height:70px;
        width:150px;
        border-radius: 40px;
        background-color: LightSeaGreen;
        color: white;
    }
    .stButton >button:hover {
        background-color: #105955;
    }
    .stButton >button p {
        font-weight: bolder !important;
        font-size: 130%;
        margin: 0;
        color:white;
    }
    .stButton >button p:hover {
        color:white;
    }
    /*Điều chỉnh phần text của thanh tìm kiếm khách sạn*/
    .hotel-info-content {
        background-color: lightskyblue;
        border-radius:40px;
        border: 1px solid Navy;
        padding-left: 20px;
        padding-top: 35px;
        height:150px;
    }
    /*Điều chỉnh phần text của phần giới thiệu*/
    .hotel-introduction {
        background-color: lightskyblue;
        border-radius:40px;
        border: 4px dashed Navy;
        padding-left: 20px;
        padding-right:20px;
        padding-top: 35px;
        font-size:140%;
        height: 900px;
        width: 1200px;
        }
    /*Điều chỉnh phần text của phần thông tin khách sạn*/
    .hotel-category-introduction {
        background-color: lightskyblue;
        border-radius:40px;
        border: 4px dashed Navy;
        padding-left: 20px;
        padding-right:20px;
        padding-top: 35px;
        font-size:140%;
        height: 300px;
        width: 1200px;
        margin: 0 0 20px 0;
        }
    .Recommendation-title {
        font-weight:bolder; 
        background-color:white;
        border-radius:60px;
        color: Darkblue;
        width:400px;
        height:100px;
        font-size:220%;
        text-align:center;
        display:flex;
        justify-content:center;
        align-items:center;
        margin: 40px 0 20px 0;
    }
    .personal-info {
        background-color: lightskyblue;
        border-radius:40px;
        border: 1px solid Navy;
        padding-left: 20px;
        padding-top: 20px;
        height:320px;
        width:420px;
        font-size:200%;
    </style>
""", unsafe_allow_html=True)



# KHỞI TẠO BIẾN LƯU TRẠNG THÁI
if 'user_name' not in st.session_state:
    st.session_state.user_name= None
if 'user_password' not in st.session_state:
    st.session_state.user_password= None
if 'mode' not in st.session_state:
    st.session_state.mode ='home'


# THANH MENU
col1,col2,col3,col4,col5,col6=st.columns(6)
with col1:
    st.image('Hotels.com_Logo_2023.png',width=200)
with col2:
    if st.button('Trang chủ',key='Main_page'):
        st.session_state.mode='home'
with col3:
    if st.button('Giới thiệu',key='introduction_page'):
        st.session_state.mode='introduction'
with col4:
    if st.button('Thông tin khách sạn',key='hotel_information'):
        st.session_state.mode='hotel_information'
with col5:
    if st.button('Đăng ký',key='Sign_up_top'):
        st.session_state.mode='signup'
with col6:
    if st.button('Đăng nhập',key='Log_in_top'):
        st.session_state.mode='login'

# BẤM VÀO TRANG CHỦ
if st.session_state.mode=='home':
    st.markdown("<hr>", unsafe_allow_html=True)
    # TẠO SOLOGAN WEB
    st.markdown("<h1 style='text-align:center;font-weight:bolder;font-size:400%'>ĐẶT PHÒNG LIỀN TAY-CHUYẾN ĐI TRONG TẦM VỚI</h1>",unsafe_allow_html=True)
    # TẠO THANH TÌM KIẾM GỒM DANH SÃCH 100 KHÁCH SẠN
    list_hotels=['Tìm kiếm khách sạn tại đây']+ut.list_hotels(100)
    selected_hotel_name=st.selectbox(label='Tìm kiếm khách sạn',options=list_hotels,label_visibility='hidden',key='Hotel_search_bar')
    # Từ khách sạn đã chọn này, người dùng có thể xem thông tin chi tiết của khách sạn
    if selected_hotel_name!='Tìm kiếm khách sạn tại đây':
        ID=ut.query_hotels_ID(selected_hotel_name)
        name=ut.hotels(ID=ID)[0]
        address=ut.hotels(ID=ID)[1]
        star=ut.hotels(ID=ID)[2]
        description=ut.hotels(ID=ID)[3]
        image_section,text_section= st.columns(2)
        with image_section:
            st.image('selected_hotel.jpg',width=340)
        with text_section:
            st.markdown(f'''<p class='hotel-info-content'>
                        <b>Tên khách sạn:</b> {name}<br>
                        <b>Địa chỉ khách sạn:</b> {address}<br>
                        <b>Số sao:</b> {star}</p>''',unsafe_allow_html=True)
            with st.expander('**Mô tả khách sạn**'):
                st.write(description)
        ut.overall_information(ID=ID)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Đề xuất khách sạn dựa vào khách sạn đã tìm kiếm 
        #st.subheader('CÓ THỂ BẠN QUAN TÂM')
        st.markdown(
        """<p class='Recommendation-title'>
                     CÓ THỂ BẠN QUAN TÂM
            </p>""",unsafe_allow_html=True)
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



# BẤM VÀO TRANG GIỚI THIỆU
elif st.session_state.mode=='introduction':
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """<p class='title-introduction' 
              style=
                    'font-weight:bolder; 
                     background-color:white;
                     border-radius:60px;
                     color: Darkblue;
                     width:260px;
                     height:100px;
                     font-size:220%;
                     text-align:center;
                     margin-bottom:2px;
                     display:flex;
                     justify-content:center;
                     align-items:center;
                     margin: 0 0 20px 0'>
                     VỀ CHÚNG TÔI
            </p>""",unsafe_allow_html=True)
    web_introduction=ut.readtxt('RECOMMENDER_BUSINESS_PROBLEM.txt')[0]
    st.markdown(f'''<p class='hotel-introduction'>{web_introduction}</p>''',unsafe_allow_html=True)

# BẤM VÀO TÌM KIẾM THÔNG TIN TÀI KHOẢNG
elif st.session_state.mode=='hotel_information':
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """<p class='title-hotel-information' 
              style=
                    'font-weight:bolder; 
                     background-color:white;
                     border-radius:60px;
                     color: Darkblue;
                     width:840px;
                     height:100px;
                     font-size:220%;
                     text-align:center;
                     display:flex;
                     justify-content:center;
                     align-items:center;
                     margin: 0 0 20px 0'>
                     LỰA CHỌN KHÁCH SẠN VÀ THÔNG TIN CẦN TRA CỨU
            </p>""",unsafe_allow_html=True)
    hotel_category_introduction=ut.readtxt('RECOMMENDER_HOTEL_CATEGORY_INTRODUCTION.txt')[0]
    st.markdown(f'''<p class='hotel-category-introduction'>{hotel_category_introduction}</p>''',unsafe_allow_html=True)
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            # Hiển thị danh sách các khách sạn
            list_hotels=ut.list_hotels(100)
            hotel_name=st.selectbox(label='#### Khách sạn',options=list_hotels)
        with col2:
            # Hiển thị các hạn mục của khách sạn
            hotel_category=['Tìm kiếm thông tin tại đây',
                            'Thông tin chung',
                            'Thông tin về lượng khách',
                            'Thông tin về loại phòng và hình thức du lịch',
                            'Thông tin về thời gian',
                            'Thông tin về điểm số',
                            'Thông tin về từ khóa']
            hotel_category_choice=st.selectbox(label='#### Thông tin',options=hotel_category)
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


# ĐĂNG KÝ TÀI KHOẢNG
elif st.session_state.mode=='signup':
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.form(key='sign_up_box'):
        st.subheader('**ĐĂNG KÝ**')
        # ĐỌC FILE KẾT QUẢ GỢI Ý CỦA ALS
        df_recommended_hotel_als=pd.read_csv('DATA_RECOMMENDATION_UI.csv')
        # DANH SÁCH TÊN CÁC REVIEWERS
        list_name_reviewer=df_recommended_hotel_als['Reviewer Name'].unique()
        name=st.selectbox(label='##### Tên đăng nhập',options=list_name_reviewer,key='sign_up_name')
        # DANH SÁCH TÊN CÁC QUỐC GIA ỨNG VỚI REVIEWERS ĐÃ CHỌN
        list_respectivve_nationality=df_recommended_hotel_als[df_recommended_hotel_als['Reviewer Name']==name]['Nationality'].unique()
        nationality=st.selectbox(label='##### Quốc tịch',options=list_respectivve_nationality,key='sign_up_nationality')
        # CÀI ĐẶT MẬT KHẨU
        password=st.text_input(label='##### Mật khẩu',placeholder='Mật khẩu',type='password',key='sign_up_password')
        # ĐIỆN THOẠI
        phone=st.text_input(label='##### Số điện thoại',placeholder='Số điện thoại',key='phone_number')
        # EMAIL
        email=st.text_input(label='##### Email',placeholder='Email',key='email')
        # GIỚI TÍNH
        sex=st.selectbox(label='##### Giới tính',options=['Nam','Nữ'],key='sex')
        # NÚT ĐĂNG KÝ
        sign_up_button=st.form_submit_button('Đăng ký')
        if sign_up_button:
            st.session_state.user_name=name
            st.session_state.user_password=password
            st.session_state.user_nationality=nationality
            st.session_state.user_phone=phone
            st.session_state.user_sex=sex
            st.session_state.user_email=email
            st.success('Bạn đã đăng ký thành công')
            st.session_state.mode='home'

# ĐĂNG NHẬP TÀI KHOẢNG
elif st.session_state.mode=='login':
    st.markdown("<hr>", unsafe_allow_html=True)
    with st.form(key='log_in_box'):
        st.subheader('**ĐĂNG NHẬP**')
        # TÊN ĐĂNG NHẬP
        name_login=st.text_input(label='##### Tên đăng nhập',key='log_in_name')
        # MẬT KHẨU
        password_login=st.text_input(label='##### Mật khẩu',placeholder='Mật khẩu',type='password',key='log_in_password')
        log_in_button=st.form_submit_button('Đăng nhập')
    if log_in_button:
        if st.session_state.user_name is None:
            st.error('Bạn chưa có tài khoản')
        if st.session_state.user_name==name_login and st.session_state.user_password==password_login:
            st.success('Bạn đã đăng nhập thành công')
            st.session_state.mode='home'

            image_section,text_section=st.columns(2)
            with text_section:
                st.markdown(f'''<p class='personal-info'>
                        <b>Tên:</b> {st.session_state.user_name}<br>
                        <b>Quốc tịch:</b> {st.session_state.user_nationality}<br>
                        <b>Giới tính:</b> {st.session_state.user_sex}<br>
                        <b>Email:</b>{st.session_state.user_email}<br>
                        <b>Số điện thoại:</b>{st.session_state.user_phone}</p>''',unsafe_allow_html=True)
            with image_section:
                st.image('avata.jpg',caption='Ảnh đại diện',width=600)
            st.markdown(
            """<p class='Recommendation-title'>
                     CÓ THỂ BẠN QUAN TÂM
            </p>""",unsafe_allow_html=True)
            df_recommended_hotel=ut.Collaborative_filtering_recommender_system(st.session_state.user_name,st.session_state.user_nationality)
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

        elif st.session_state.user_name!=name_login:
            st.error('Sai tên đăng nhập hãy đăng nhập lại')
        elif st.session_state.user_password!=password_login:

            st.error('Sai mật khẩu hãy đăng nhập lại')


