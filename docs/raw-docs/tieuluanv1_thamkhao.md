**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**

**KHOA CÔNG NGHỆ THÔNG TIN 1**

# \--o0o--

# KIẾN TRÚC VÀ THIẾT KẾ PHẦN MỀM

**TIỂU LUẬN VERSION 01**

Giảng viên : Trần Đình Quế

Khóa : 2022-2027

Hệ : Đại học chính quy

Chuyên ngành : Công nghệ phần mềm

Hà Nội, 2026

# MỤC LỤC

[MỤC LỤC 2](#_bookmark0)

[CHƯƠNG 1: TỪ MONOLITHIC ĐẾN MICROSERVICES VÀ DDD 1](#_bookmark1)

- 1.  [Giới thiệu Monolithic Architecture 1](#_bookmark2)
        1.  [Khái niệm 1](#_bookmark3)
        2.  [Cấu trúc điển hình 1](#_bookmark4)
        3.  [Ví dụ thực tế 2](#_bookmark5)
        4.  [Nhược điểm chi tiết 3](#_bookmark6)
        5.  [Khi nào nên dùng Monolithic 3](#_bookmark7)
    2.  [Microservices Architecture 4](#_bookmark8)
        1.  [Khái niệm 4](#_bookmark9)
        2.  [Đặc điểm 5](#_bookmark10)
        3.  [So sánh Monolithic vs Microservices 5](#_bookmark11)
        4.  [Ưu điểm 6](#_bookmark12)
        5.  [Nhược điểm 6](#_bookmark13)
        6.  [Nguyên tắc thiết kế 7](#_bookmark14)
    3.  [Domain Driven Design (DDD) 8](#_bookmark15)
        1.  [Mục tiêu 8](#_bookmark16)
        2.  [Các khái niệm cốt lõi 8](#_bookmark17)
        3.  [Context Map 10](#_bookmark18)
        4.  [DDD trong Microservices 11](#_bookmark19)
    4.  [Case Studey: Healthcare 11](#_bookmark20)
        1.  [Mô tả bài toán 11](#_bookmark21)
        2.  [Bước 1: Xác định Domain 12](#_bookmark22)
        3.  [Bước 2: Xác định Bounded Context 13](#_bookmark23)
        4.  [Bước 3: Phân rã thành Microservices 14](#_bookmark24)
        5.  [Bước 4: Xác định quan hệ 14](#_bookmark25)
        6.  [Ví dụ API 15](#_bookmark26)
    5.  [Kết luận 16](#_bookmark27)

[CHƯƠNG 2: PHÁT TRIỂN HỆ E-COMMERCE MICROSERVICE 17](#_bookmark28)

- 1.  [Xác định yêu cầu 17](#_bookmark29)
        1.  [Functional Requirements 17](#_bookmark30)
        2.  [Non-functional Requirements 17](#_bookmark31)
    2.  [Phân rã hệ thống theo DDD 18](#_bookmark32)
        1.  [Bounded Context 18](#_bookmark33)
        2.  [Nguyên tắc 19](#_bookmark34)
    3.  [Thiết kế Product Service (Django) 20](#_bookmark35)
    4.  [Thiết kế User Service (Django) 24](#_bookmark36)
    5.  [Thiết kế Cart Service 28](#_bookmark37)
    6.  [Thiết kế Order Service 30](#_bookmark38)
    7.  [Thiết kế Payment Service 35](#_bookmark39)
    8.  [Thiết kế Shipping Service 38](#_bookmark40)
    9.  [Luồng hệ thống tổng thể 41](#_bookmark41)
    10. [Kết luận 42](#_bookmark42)

[CHƯƠNG 3: AI SERVICE CHO TƯ VẤN SẢN PHẨM 43](#_bookmark43)

- 1.  [Mục tiêu 43](#_bookmark44)
    2.  [Kiến trúc AI service 43](#_bookmark45)
    3.  [Thu thập dữ liệu 44](#_bookmark46)
        1.  [User Behavior Data 44](#_bookmark47)
        2.  [Ví dụ dataset 45](#_bookmark48)
    4.  [Mô hình LSTM (Sequence Modeling) 46](#_bookmark49)
        1.  [Ý tưởng 46](#_bookmark50)
        2.  [Model chi tiết 47](#_bookmark51)
        3.  [Training 48](#_bookmark52)
    5.  [Knowledge Graph với Neo4j 49](#_bookmark53)
        1.  [Mô hình đồ thị 49](#_bookmark54)
        2.  [Ví dụ Cypher 51](#_bookmark55)
        3.  [Truy vấn gợi ý 51](#_bookmark56)
    6.  [RAG (Retrieval-Augmented Generation) 52](#_bookmark57)
        1.  [Pipeline 52](#_bookmark58)
        2.  [Vector Database 52](#_bookmark59)
        3.  [Ví dụ 53](#_bookmark60)
    7.  [Kết hợp Hybrid Model 53](#_bookmark61)
    8.  [Hai dạng AI Service 54](#_bookmark62)
        1.  [Recommendation List 54](#_bookmark63)
        2.  [Chatbot tư vấn 55](#_bookmark64)
    9.  [Triển khai AI Service 56](#_bookmark65)
        1.  [Tech stack 56](#_bookmark66)
        2.  [Kiến trúc 56](#_bookmark67)
    10. [Kết luận 57](#_bookmark68)

[CHƯƠNG 4: XÂY DỰNG HỆ THỐNG HOÀN CHỈNH 59](#_bookmark69)

- 1.  [Kiến trúc tổng thể 59](#_bookmark70)
        1.  [Mô hình hệ thống 59](#_bookmark71)
        2.  [Nguyên tắc 59](#_bookmark72)
    2.  [System Architecture 59](#_bookmark73)
        1.  [Overview 59](#_bookmark74)
        2.  [Microservice Architecture 60](#_bookmark75)
        3.  [API Gateway 60](#_bookmark76)
        4.  [Service Communication 61](#_bookmark77)
        5.  [Containerization and Deployment 61](#_bookmark78)
        6.  [System Structure 62](#_bookmark79)
        7.  [Design Principles 62](#_bookmark80)
        8.  [Security Considerations 63](#_bookmark81)
        9.  [Discussion 63](#_bookmark82)
    3.  [API Gateway (Nginx) 64](#_bookmark83)
        1.  [Vai trò 64](#_bookmark84)
        2.  [Cấu hình mẫu 65](#_bookmark85)
    4.  [Authentication (JWT) 65](#_bookmark86)
    5.  [Giao tiếp giữa các Service 66](#_bookmark87)
    6.  [Docker hóa hệ thống 67](#_bookmark88)
        1.  [Dockerfile (Django) 67](#_bookmark89)
        2.  [docker-compose.yml 68](#_bookmark90)
    7.  [Luồng hệ thống (End-to-End) 68](#_bookmark91)
        1.  [Use case: Mua hàng 68](#_bookmark92)
        2.  [Sequence logic 69](#_bookmark93)

[KẾT LUẬN 70](#_bookmark94)


## Nguyên tắc thiết kế

Ba nguyên tắc thiết kế cốt lõi định hình nên ranh giới vật lý và logic của kiến trúc Microservices. Sự vi phạm bất kỳ nguyên tắc nào trong số này đều trực tiếp làm hệ thống thoái hóa thành một mớ code Monilithic phân tán, nơi gánh chịu Nhược điểm của cả hai mô hình.

_Thứ nhất, Đơn nhiệm (Single Responsibility Principle - SRP)._ Nguyên lý này quy định một service chỉ được phép có một lý do duy nhất để thay đổi,. Dưới góc độ triển khai, SRP ép buộc kỹ sư phải phân rã các nghiệp vụ độc lập vào các ranh giới dịch vụ chuyên biệt. Mặc dù làm tăng số lượng repository cần quản lý, SRP thu nhỏ đáng kể kích thước của từng dịch vụ, từ đó cô lập lỗi và tăng độ ổn định của tiến trình. Việc nhồi nhét nhiều tính năng vào cùng một tiến trình sẽ phá vỡ nguyên lý này, khiến một thay đổi ở logic giao hàng có thể làm hỏng chức năng thanh toán.

_Thứ hai, Phụ thuộc lỏng lẻo (Loose Coupling)._ Coupling đo lffờng mức độ phụ thuộc và dính líu chéo giữa các thành phần phần mềm. Để đạt được loose coupling, kiến trúc Microservices thiết lập các ranh giới giao tiếp cứng bằng API, che giấu hoàn toàn cấu trúc mã nguồn nội bộ,. Đặc biệt, nguyên tắc này cấm tuyệt đối việc chia sẻ cơ sở dữ liệu chung. Mỗi dịch vụ phải quản lý một vùng dữ liệu độc quyền. Bằng cách giấu đi chi tiết cài đặt, kỹ sư có thể tái cấu trúc hoặc thay đổi bảng dữ liệu của dịch vụ Đơn hàng mà không tạo ra hiệu ứng dây chuyền làm sập dịch vụ Khách hàng, Sự đánh đổi của mức độ phụ thuộc thấp này là kỹ sư không thể tận dụng cơ chế khóa cơ sở dữ liệu truyền thống, buộc phải xử lý tính nhất quán dữ liệu xuyên mạng,.

_Thứ ba, Độ gắn kết cao (High Cohesion)._ Cohesion đo lffờng sự tập trung vào một nhiệm vụ duy nhất của các thành phần bên trong một module. Trong môi Trường phân tán, High Cohesion hoạt động như lực hướng tâm, kết hợp chặt chẽ với nguyên tắc Đóng chung (Common Closure Principle

\- CCP),. Nguyên tắc này yêu cầu gom tất cả các class, tính năng hoặc module thường xuyên thay đổi cùng nhau vì một lý do nghiệp vụ vào chung một dịch vụ triển khai,. Thay vì để các logic liên quan bị băm nhỏ và nằm rải rác trên nhiều dịch vụ (gây ra hiện tượng gọi chéo liên tục qua mạng),

độ gắn kết cao đảm bảo rằng khi một quy tắc kinh doanh thay đổi, chi phí sửa chfia và triển khai được khoanh vùng tối đa bên trong đúng một dịch vụ duy nhất

## Domain Driven Design (DDD)Mục tiêu

Mục tiêu cốt lõi của Domain-Driven Design (DDD) là kiểm soát sự phức tạp của phần mềm bằng cách đặt mô hình nghiệp vụ làm trung tâm của toàn bộ kiến trúc, tách biệt hoàn toàn khỏi các quyết định về công nghệ hạ tầng. Thay vì để cấu trúc cơ sở dữ liệu hay bộ framework nền tảng dẫn dắt thiết kế, DDD ép buộc mã nguồn và cấu trúc hệ thống phải phản ánh chính xác lăng kính nghiệp vụ thực tế.

Để thực thi sự đồng nhất này, DDD thiết lập một mục tiêu phụ trợ mang tính sống còn: xây dựng Ngôn ngữ chung. Kỹ sư phần mềm và chuyên gia nghiệp vụ buộc phải sử dụng chung một tập từ vựng thống nhất trong mọi tài liệu, thảo luận và mã nguồn. Hệ quả kỹ thuật của mục tiêu này là rào cản dịch thuật giữa yêu cầu kinh doanh và logic code được triệt tiêu, giúp mã nguồn trở thành tài liệu mô tả nghiệp vụ sống động và chính xác nhất.

Dưới góc độ phân rã hệ thống, cách tiếp cận truyền thống thường nỗ lực xây dựng một mô hình dữ liệu toàn cục cho toàn bộ tổ chức. Mặc dù tạo ra cảm giác thống nhất trên lý thuyết, nhưng thực tế triển khai lại dẫn đến sự phình to và xung đột logic nghiêm trọng khi các phân hệ khác nhau có định nghĩa khác biệt về cùng một thực thể (ví dụ: thực thể 'User' trong hệ thống Đặt hàng rất khác với 'User' trong hệ thống Thanh toán). DDD phá vỡ rào cản này bằng mục tiêu phân rã không gian vấn đề thành các miền con độc lập. Mỗi miền con được ánh xạ vào một Không gian giới hạn (Bounded Context) riêng biệt, nơi mô hình nghiệp vụ chỉ có giá trị và ý nghĩa duy nhất bên trong ranh giới đó.

Mục tiêu chia rã và cô lập mô hình của DDD chính là nền tảng kỹ thuật để giải quyết bài toán khó nhất trong kiến trúc Microservices: xác định ranh giới dịch vụ. Bằng cách thiết lập các ranh giới Bounded Context chặt chẽ, DDD ngăn chặn sự hình thành của các lớp khổng lồ (God classes) ôm đồm quá nhiều logic, triệt tiêu sự phụ thuộc chéo giữa các phân hệ và bảo vệ tính tự trị của dữ liệu.

## Các khái niệm cốt lõi

Để chuyển hóa các yêu cầu nghiệp vụ phức tạp thành mã nguồn, phân tích 4 khái niệm kỹ thuật cốt lõi đóng vai trò định hình kiến trúc của DDD.

- - - - _Thứ nhất, Entity (Thực thể):_ Entity là các đối tượng nghiệp vụ mang một định danh duy nhất (ID) và không thể thay đổi trong suốt vòng đời, bất chấp sự biến động của các thuộc tính bên trong. Hai thực thể dù có mọi giá trị thuộc tính giống hệt nhau nhưng mang ID khác nhau thì vẫn là hai vùng nhớ và hai bản ghi cơ sở dữ liệu hoàn toàn độc lập. Điển hình như thực thể User hay Product. Việc thiết kế Entity đòi hỏi hệ thống phải duy trì cơ chế quản lý vòng đời và tính nhất quán của ID xuyên suốt các luồng giao dịch phân tán.
            - _Thứ hai, Value Object (Đối tượng giá trị)._ Trái ngược với Entity, Value Object hoàn toàn

không có định danh. Bản sắc của chúng được định đoạt hoàn toàn bởi tập hợp các giá trị thuộc tính cấu thành. Ví dụ tiêu biểu là Address hoặc Money. Bản chất kỹ thuật của Value

Object là tính bất biến. Khi một thuộc tính của Value Object cần thay đổi, kỹ sư không được phép cập nhật trực tiếp trên vùng nhớ hiện tại mà bắt buộc phải hủy đối tượng cũ và khởi tạo một đối tượng mới hoàn toàn. Đặc tính bất biến này loại bỏ hoàn toàn các lỗi rò rỉ trạng thái khi truyền dữ liệu giữa các luồng xử lý đồng thời.

- - - - _Thứ ba, Aggregate và Aggregate Root (Cụm tập hợp)._ Bóc tách Aggregate như một cụm

(cluster) gồm các Entity và Value Object liên quan chặt chẽ với nhau, được hệ thống đóng gói và xử lý như một đơn vị nguyên khối về mặt giao dịch. Mỗi Aggregate luôn có một Entity trung tâm kiểm soát gọi là Aggregate Root. Xét ví dụ cụm Order (đóng vai trò Root) quản lý danh sách các OrderItem. Nguyên tắc thiết kế bắt buộc là các hệ thống bên ngoài không được phép tham chiếu trực tiếp đến OrderItem, mà chỉ được gọi thông qua Order. Ràng buộc định tuyến này ép buộc mọi thao tác cập nhật (update/delete) phải đi qua Root, cho phép hệ thống duy trì tính toàn vẹn dữ liệu chỉ bằng một giao dịch cơ sở dữ liệu cục bộ duy nhất, thay vì phải rải lệnh khóa bảng ra nhiều thực thể rời rạc.

- - - - _Cuối cùng, Bounded Context (Không gian giới hạn)._ Đây là ranh giới logic và vật lý bao

bọc lấy một mô hình nghiệp vụ, đảm bảo các khái niệm bên trong nó có tính toàn vẹn tuyệt đối và không bị chồng chéo. Thay vì thiết kế một siêu thực thể (God class) User khổng lồ chfía mọi cột dữ liệu của toàn doanh nghiệp, Bounded Context bẻ gãy hệ thống thành nhiều không gian hẹp. User trong User Context tập trung vào logic định danh và mật khẩu, trong khi User tại Order Context chỉ lưu trữ địa chỉ và lịch sử giao dịch. Bằng cách cô lập dữ liệu và ngữ nghĩa vào các ranh giới khép kín, Bounded Context triệt tiêu sự phụ thuộc chéo giữa các miền nghiệp vụ, tạo ra nền tảng kỹ thuật chính xác nhất để cắt chia hệ thống thành các Microservices

## Context Map

Context Map là công cụ kiến trúc dùng để trực quan hóa mạng lffới giao tiếp và mức độ phụ thuộc giữa các Bounded Context. Khi phân rã một hệ thống thành các miền nghiệp vụ độc lập, dữ liệu không thể tồn tại cô lập mà buộc phải luân chuyển qua lại. Context Map không chỉ vạch ra ranh giới vật lý mà còn xác định rõ các ràng buộc hợp tác giữa các nhóm kỹ sư. Dựa trên bản chất tích hợp, bóc tách hai mô hình quan hệ cốt lõi là Shared Kernel và Customer-Supplier.

_Thứ nhất, quan hệ Shared Kernel._ Mô hình này xuất hiện khi hai hoặc nhiều Bounded Context thỏa hiệp dùng chung một tập hợp mã nguồn, mô hình domain hoặc dùng chung một bảng cơ sở dữ liệu. Về mặt kỹ thuật, việc chia sẻ này loại bỏ chi phí chuyển đổi dữ liệu qua lại và giảm thiểu độ trễ mạng, giúp vòng lặp gọi hàm diễn ra nhanh chóng. Tuy nhiên, sự đánh đổi là hệ thống phải gánh chịu mức độ phụ thuộc cực cao. Mọi thay đổi cấu trúc trên phần Shared Kernel từ một đội ngũ đều yêu cầu sự đồng bộ kiểm thứ nghiêm ngặt; nếu không, mã nguồn của các đội khác sẽ lập tfíc phát sinh lỗi biên dịch hoặc lỗi runtime.

_Thứ hai, quan hệ Customer-Supplier._ Đây là mô hình thiết lập luồng phụ thuộc một chiều từ thượng nguồn xuống hạ nguồn (upstream-downstream). Miền Supplier (thượng nguồn) định đoạt mô hình dữ liệu và phơi bày chúng qua các hợp đồng giao tiếp (API Contracts). Miền Customer (hạ nguồn) là bên tiêu thụ và phải điều chỉnh luồng xử lý của mình theo API đó. Hệ quả kỹ thuật của luồng giao tiếp này là sự rủi ro mất tự trị: nếu Supplier cấu trúc lại API trả về mà không báo trước, tiến trình của Customer sẽ lập tfíc sụp đổ.

Để hóa giải điểm nghẽn phụ thuộc trong mô hình Customer-Supplier, hệ thống hạ nguồn (Customer) bắt buộc phải thiết lập một Lớp chống tham nhũng (Anti-Corruption Layer - ACL). Lớp ACL đóng vai trò như một màng lọc dịch thuật trung gian, đảm nhiệm việc ánh xạ mô hình thượng nguồn sang ngôn ngữ và cấu trúc của hạ nguồn. Mặc dù làm tăng độ trễ xử lý do tốn thêm

một nhịp chuyển đổi dữ liệu, ACL tạo ra một ranh giới bảo vệ cứng. Khi Supplier thay đổi cấu trúc API, kỹ sư chỉ cần cập nhật logic tại lớp màng lọc ACL, bảo vệ toàn vẹn logic nghiệp vụ cốt lõi bên trong Customer khỏi việc phải đập bỏ và viết lại tốn kém.

## DDD trong Microservices

Sự hội tụ giữa Domain-Driven Design (DDD) và Microservices là sự khớp nối hoàn hảo giữa logic và vật lý. Trong DDD, Bounded Context khoanh vùng một mô hình nghiệp vụ khép kín; khi đffa vào môi Trường phân tán, mỗi Bounded Context này trực tiếp đóng vai trò là bản thiết kế định hình ranh giới vật lý của một microservice độc lập,. Hệ quả là một đội ngũ kỹ sư có toàn quyền sở hfiu mô hình, tự do phát triển và triển khai domain đó mà không phải chịu rủi ro xung đột mã nguồn với các đội khác.

Việc ánh xạ 1-1 giữa Bounded Context và Microservice giải quyết triệt để rào cản về siêu lớp (God classes) thường thấy ở hệ thống cũ,. Thay vì bị ép dùng chung một thực thể Order khổng lồ ôm đồm toàn bộ dữ liệu doanh nghiệp, DDD bẻ gãy nó thành các khái niệm hẹp hơn. Phân hệ Thanh toán và phân hệ Giao hàng sẽ tự định nghĩa cấu trúc Order theo đúng lăng kính nghiệp vụ của mình; ví dụ Order trong Delivery Service chỉ lưu trữ duy nhất thông tin địa chỉ và thời gian lấy/giao hàng. Sự phân mảnh chủ đích này chính là nền tảng kỹ thuật bắt buộc để hệ thống duy trì được mức độ phụ thuộc thấp thông qua nguyên tắc mỗi service một cơ sở dữ liệu riêng.

Dưới góc độ cấu trúc: phân rã hệ thống theo chiều dọc của miền nghiệp vụ, tuyệt đối tránh cắt chia theo chiều ngang của tầng kỹ thuật,. Nếu kiến trúc bị chia theo lớp kỹ thuật—ví dụ như xây dựng riêng một service chuyên xử lý giao diện, một service chfía quy tắc nghiệp vụ, và một service chuyên truy xuất dữ liệu—thì một khái niệm nghiệp vụ như "Thanh toán giỏ hàng" sẽ bị bôi bẩn, phân tán rải rác trên toàn mạng lffới. Khi có thay đổi về quy trình, kỹ sư buộc phải chỉnh sửa và triển khai đồng loạt hàng loạt các service này, trực tiếp phá vỡ đặc tính triển khai độc lập của Microservices.

Nguyên tắc thiết kế tối hậu: Ranh giới logic của DDD phải làm tiêu chuẩn để rạch ranh giới vật lý cho Microservices; mọi sự thỏa hiệp cắt chia theo ranh giới công nghệ thay vì lăng kính nghiệp vụ đều là một thiết kế lỗi, chắc chắn sẽ đẩy hệ thống thoái hóa thành mớ nguyên khối phân tán.


# CHƯƠNG 2: PHÁT TRIỂN HỆ E-COMMERCE MICROSERVICE

## Xác định yêu cầuFunctional Requirements

- - - - _Quản lý sản phẩm._ Hệ thống phải kiểm soát vòng đời của các mặt hàng thuộc các phân hệ độc lập: book, electronics, fashion.
            - _Quản lý người dùng._ Hệ thống quản lý luồng định danh và phân quyền dựa trên vai trò

(RBAC) cho ba nhóm tài khoản: admin, staff và customer.

- - - - _Giỏ hàng._ Hệ thống cho phép người dùng thao tác thêm, cập nhật số lượng và xóa sản phẩm.
            - _Đặt hàng._ Hệ thống thực thi luồng chuyển đổi trạng thái từ giỏ hàng sang đơn hàng.
            - _Thanh toán và Giao hàng._ Hệ thống phải theo dõi vòng đời giao dịch tài chính (Pending, Success, Failed) và trạng thái luân chuyển hàng hóa vật lý (Processing, Shipping, Delivered). Luồng nghiệp vụ này yêu cầu tính nhất quán dữ liệu khắt khe. Nếu tiến trình thanh toán thất bại, hệ thống bắt buộc phải có luồng hoàn tác kích hoạt ngược lại Order Service để hủy đơn hàng và nhả tồn kho.
            - _Tìm kiếm và Gợi ý sản phẩm bằng AI._ Khác biệt hoàn toàn với các truy vấn CRUD thông

thường, hệ thống phải thu thập dữ liệu hành vi (view, click, add-to-cart, ...) theo thời gian thực để trả về danh sách sản phẩm cá nhân hóa và cung cấp tính năng chatbot tư vấn.

## Non-functional Requirements

- - - - _Khả năng mở rộng (Scalability)._ Hệ thống phân tán từ bỏ hoàn toàn việc nhân bản toàn bộ ứng dụng lãng phí của mô hình Monolithic. Thay vào đó, kiến trúc áp dụng chiến lược mở rộng trục Y (Y-axis scaling) để băm nhỏ dịch vụ và định tuyến tài nguyên chính xác đến điểm nghẽn. Ví dụ, trong các đợt Flash Sale, hệ thống chỉ cần cấu hình tự động mở rộng (auto-scaling) thêm instance cho Order Service và Cart Service, trong khi User Service giữ nguyên cấu hình. Mặc dù tối ưu hóa triệt để chi phí phần cứng, thiết kế này ép buộc hạ tầng phải tích hợp cơ chế Service Discovery và Load Balancing động để liên tục cập nhật địa chỉ IP của các instance mới sinh ra.
            - _Tính sẵn sàng cao (High Availability)._ Bản chất phân tán sinh ra rủi ro lỗi cục bộ do độ trễ

hoặc đfít gãy mạng. Để đảm bảo luồng mua sắm của khách hàng hoạt động 24/7, kiến trúc phải thiết lập các màng lọc cách ly lỗi. Nếu Payment Service quá tải và treo, hệ thống không được phép để request tạo đơn hàng của Order Service bị kéo sập theo. Kỹ sư bắt buộc phải bọc các lời gọi mạng bằng Circuit Breaker, Timeouts, Sự đánh đổi ở đây là hệ thống

phải chấp nhận phá vỡ tính nhất quán tfíc thời (strong consistency), tạm thời lưu trạng thái đơn hàng và xử lý bù trữ sau (eventual consistency) để giữ cho giao dịch cốt lõi không bị gián đoạn.

- - - - _Bảo mật (Security) theo hướng phi trạng thái._ Phân rã dịch vụ đồng nghĩa với việc ranh

giới mạng nội bộ được mở rộng, dẫn đến rủi ro lộ lọt dữ liệu giữa các luồng giao tiếp. Kiến trúc giải quyết vấn đề này thông qua cơ chế xác thực phi trạng thái bằng JSON Web Tokens (JWT). API Gateway đóng vai trò chốt chặn đầu tiên, sau khi xác thực sẽ đẩy JWT chfía thông tin phân quyền (RBAC) xuống các microservices phía sau. Mỗi service tự giải mã và

thẩm định quyền truy cập từ token mà không cần tạo request gọi ngược về User Service. Cơ chế này triệt tiêu hoàn toàn điểm nghẽn cổ chai về hiệu năng, nhưng bù lại, hệ thống phải đối mặt với rủi ro bảo mật khó nhằn: JWT không thể bị thu hồi ngay lập tfíc trước khi hết hạn, buộc kỹ sư phải thiết kế thêm cơ chế Blacklist hoặc sử dụng Refresh Token phức tạp.

- - - - _Khả năng bảo trì (Maintainability)._ Việc xé nhỏ hệ thống tạo ra mức độ phụ thuộc lỏng lẻo

giúp thu hẹp phạm vi ảnh hffởng của mỗi bản cập nhật. Kỹ sư có thể sửa mã nguồn hoặc thay đổi cấu trúc bảng database của Product Service mà không làm hỏng Cart Service. Khối lượng code nhỏ cũng giúp tăng tốc độ biên dịch và khởi động tiến trình. Tuy nhiên, khả năng bảo trì cục bộ này lại sinh ra lực cản lớn ở khâu vận hành tổng thể. Để gỡ lỗi một request bị lỗi khi nó nhảy cóc qua 4 services khác nhau, hệ thống bắt buộc phải tốn chi phí tài nguyên để cấy ghép các công cụ giám sát phân tán (Observability) như Distributed Tracing và Log Aggregation. Thiếu đi hạ tầng này, Microservices sẽ biến thành một hộp đen không thể bảo trì.

### Phân rã hệ thống theo DDD

## Bounded Context

Dựa trên phân tích yêu cầu chức năng, hệ thống E-commerce được định tuyến thành 7 Bounded Context cốt lõi:

- - - - _User Context._ Ngữ cảnh này tập trung toàn bộ logic định danh, xác thực và phân quyền (RBAC) cho mọi đối tượng (Admin, Staff, Customer). Việc gộp chung các vai trò này vào một miền duy nhất thay vì băm nhỏ theo từng loại người dùng giúp bảo toàn tính gắn kết. Thiết kế này triệt tiêu các luồng gọi chéo liên tục qua mạng khi hệ thống cần kiểm tra quyền truy cập của một tác vụ nội bộ.

- - - - _Product Context._ Ngữ cảnh này bọc gói toàn bộ vòng đời của sản phẩm, bao gồm thông tin danh mục (catalog), thuộc tính biến thể và tồn kho. Dưới góc độ DDD, ranh giới thiết kế bắt buộc phải dựa trên hành vi hệ thống, tuyệt đối không tách service theo từng loại sản phẩm vật lý (như Phone Service hay Laptop Service). Cách tiếp cận gom cụm này đảm bảo tính tự trị của dữ liệu sản phẩm, tránh hiện tượng thoái hóa hiệu năng do phải join bảng liên mạng khi khách hàng tìm kiếm toàn dải sản phẩm.
            - _Cart Context._ Giỏ hàng hoạt động như một vùng đệm lưu trữ tạm thời trước khi chốt đơn.

Đặc thù của ngữ cảnh này là tần suất thao tác đọc/ghi (I/O) cực kỳ dày đặc nhưng dữ liệu lại có vòng đời ngắn. Việc tách rời Cart Context thành một ranh giới riêng cho phép kỹ sư tùy biến hạ tầng độc lập, ví dụ sử dụng cơ chế lưu trữ trên RAM (In-memory caching như Redis) thay vì cơ sở dữ liệu quan hệ, ngăn chặn tình trạng thắt cổ chai I/O đánh sập database chính.

- - - - _Thứ tư, Order Context._ Đây là ngữ cảnh điều phối giao dịch trung tâm. Order Context tuyệt

đối không lưu trữ dữ liệu chi tiết của sản phẩm hay người dùng, mà chỉ nắm giữ định danh (ID) để ráp nối luồng nghiệp vụ. Bằng cách thiết lập ranh giới cứng này, luồng tạo đơn hàng bắt buộc phải giao tiếp qua mạng thông qua các mẫu thiết kế Saga, đánh đổi một phần độ trễ mạng để đổi lấy tính nhất quán dữ liệu phân tán an toàn.

- - - - _Payment Context._ Ngữ cảnh thanh toán bọc gói mọi tương tác phức tạp với các cổng thanh

toán bên thứ ba. Sự cô lập vật lý này thiết lập một màng lọc chịu lỗi hoàn hảo. Nếu API của đối tác thanh toán gián đoạn, sự cố bị giam lỏng bên trong Payment Context; luồng duyệt sản phẩm và thêm vào giỏ hàng của người dùng hoàn toàn không bị ảnh hffởng.

- - - - _Shipping Context._ Việc tách biệt hoàn toàn miền vận chuyển khỏi miền đơn hàng xuất phát

từ sự khác biệt về vòng đời dữ liệu. Nghiệp vụ Order kết thúc khi thanh toán thành công, trong khi Shipping tiếp tục theo dõi luồng luân chuyển vật lý dài ngày (Processing, Shipping, Delivered). Sự phân tách này bẻ gãy God Class Order cũ, tránh việc một bảng dữ liệu duy nhất phải gánh vác quá nhiều trạng thái nghiệp vụ trái ngược nhau.

## Nguyên tắc

Để đảm bảo ranh giới Bounded Context không bị phá vỡ khi chuyển hóa thành các microservices vật lý, kiến trúc hệ thống buộc phải tuân thủ hai nguyên tắc thiết kế cứng rắn.

- - - - _Thứ nhất, mỗi context phải sở hữu một cơ sở dữ liệu riêng._ Để đạt được tính tự trị dữ liệu, cơ sở dữ liệu buộc phải bị phân mảnh vật lý cho từng Bounded Context. Mỗi service nắm toàn quyền kiểm soát read/write trên database của mình; các service khác tuyệt đối không được phép truy xuất trực tiếp vào cấu trúc bảng này. Việc chia tách này triệt tiêu hoàn toàn rủi ro cạn kiệt connection pool chéo, nhưng đánh đổi lại, hệ thống mất đi khả năng sử dụng giao dịch cơ sở dữ liệu tập trung, ép buộc kỹ sư phải xử lý tính nhất quán dữ liệu phân tán bằng các mẫu thiết kế phức tạp như Saga.
            - _Thứ hai, giao tiếp chéo bắt buộc thông qua REST API._ Khi ranh giới dữ liệu bị đóng kín,

các lời gọi truy vấn chéo schema biến mất, luồng nghiệp vụ bắt buộc phải luân chuyển dữ liệu xuyên mạng thông qua các hợp đồng API. Bằng cách phơi bày dữ liệu qua REST API, các service che giấu hoàn toàn chi tiết cài đặt nền tảng, cho phép đội ngũ phát triển tự do thay đổi công nghệ bên dưới mà không làm gãy vỡ các service gọi đến. Thiết kế này bảo

vệ toàn vẹn logic của miền, nhưng trực tiếp làm phát sinh độ trễ mạng và phơi bày hệ thống trước rủi ro lỗi cục bộ. Hệ quả tất yếu là kỹ sư không thể thiết kế hệ thống với giả định mạng luôn ổn định; mọi lời gọi REST API đồng bộ đều bắt buộc phải được bọc bởi cơ chế ngắt Circuit Breaker để ngăn chặn hiện tượng treo luồng và sụp đổ dây chuyền

## Thiết kế Product Service (Django)

### Bước 1: Xác định lớp

Các thực thể bên trong Product Context được xác định không chỉ bao gồm thông tin hàng hóa mà còn bọc gói các domain phụ trợ liên quan trực tiếp đến vòng đời hiển thị của sản phẩm.

- Lớp trung tâm (Aggregate Root): Product. Đây là điểm nghẽn truy xuất; mọi thao tác cập nhật thông tin hàng hóa đều phải đi qua lớp này.
- Lớp danh mục: Category. Quản lý cấu trúc phân cấp dữ liệu, không chfía business logic

phức tạp.

- Lớp kế thừa (Đặc thù ngành hàng): Book, Electronics, Fashion. Thiết kế này giải quyết sự khác biệt về cấu trúc dữ liệu của từng loại sản phẩm.
- Lớp biến thể: Variant. Xử lý bài toán một sản phẩm có nhiều phiên bản (kích thước, màu

sắc) có mức giá hoặc tồn kho khác nhau.

- Lớp phụ thuộc: Review. gộp dịch vụ đánh giá. Việc nằm chung context giúp loại bỏ các lệnh gọi mạng (RPC) khi cần join dữ liệu hiển thị chi tiết sản phẩm cùng đánh giá.

### Bước 2: Xác định thuộc tính (Attributes)

Cấu trúc thuộc tính đòi hỏi sự linh hoạt tối đa. Bảng Product cốt lõi chỉ lưu các Trường dữ liệu chung nhất. Các Trường đặc thù được đẩy xuống các lớp con hoặc xử lý qua kiểu dữ liệu phi cấu trúc (JSONB).

- Lớp Product
    - id: int (Primary Key)
    - sku: string (Mã định danh kho)
    - name: string
    - base_price: float
    - stock: int
    - attributes: JSONB (Lưu trữ linh hoạt các thuộc tính không cố định như thông số kỹ thuật động, loại bỏ thiết kế bảng thưa - sparse tables).
- Lớp Category
    - id: int
    - name: string
    - parent_id: int (Tự tham chiếu để tạo cây danh mục)

- Lớp Book (Kế thừa Product)
    - author: string
    - isbn: string
    - publisher: string
- Lớp Electronics (Kế thừa Product)
    - brand: string
    - warranty_months: int
- Lớp Fashion (Kế thừa Product)
    - material: string
    - gender: string
- Lớp Variant
    - id: int
    - sku: string (SKU riêng cho từng biến thể)
    - additional_price: float (Giá cộng dồn so với base_price)
    - color: string
    - size: string
- Lớp Review
    - id: int
    - user_id: int (Lưu ý: Chỉ lưu ID, tuyệt đối không tham chiếu object User để giữ loose coupling vật lý với User Service).
    - rating: int
    - content: string

### Bước 3: Xác định quan hệ

- Association: Product → Category
    - Ký hiệu: 0..\* → 1..1 (Hoặc 1..\* qua bảng trung gian nếu một sản phẩm thuộc nhiều danh mục).
    - Giải thích: Một danh mục (Category) chfía nhiều sản phẩm (Product), nhưng để đơn giản hóa luồng truy xuất, một sản phẩm thuộc về một danh mục định tuyến chính.
- Inheritance (Generalization): Book, Electronics, Fashion → Product
    - Giải thích: Đây là quan hệ "is-a" (a-kind-of). Dưới góc độ hạ tầng CSDL quan hệ (RDBMS) như PostgreSQL, mô hình kế thừa này được hiện thực hóa bằng kỹ thuật phân mảnh (table-per-type) sử dụng OneToOneField trỏ ngược ID về bảng Product gốc.
- Composition: Product → Variant
    - Ký hiệu: 1..1 → 1..\* (Hình thoi đặc bên phía Product).
    - Giải thích: Quan hệ "has-parts" vòng đời phụ thuộc vật lý. Một Variant không thể tồn tại độc lập nếu Product gốc bị xóa. Toàn bộ thao tác cập nhật tồn kho hay giá của Variant bắt buộc phải gọi qua Aggregate Root là Product.
- Composition: Product → Review

- - Ký hiệu: 1..1 → 0..\* (Hình thoi đặc bên phía Product).
    - Giải thích: Đánh giá (Review) sinh ra để miêu tả một sản phẩm cụ thể. Xóa sản phẩm sẽ trigger luồng xóa toàn bộ đánh giá đi kèm nhằm bảo vệ tính toàn vẹn dữ liệu (data integrity).

## Thiết kế User Service (Django)

### Bước 1: Xác định lớp

User Context khoanh vùng các lớp dữ liệu trực tiếp định hình danh tính và quyền hạn của người dùng trong hệ thống.

- Lớp trung tâm (Aggregate Root): User. Thực thể nòng cốt kiểm soát vòng đời tài khoản và dữ liệu đăng nhập.
- Lớp kế thừa (Đặc thù vai trò): Customer, Staff, Admin. Tách biệt logic và dữ liệu đặc thù

của từng nhóm người dùng, tránh việc nhồi nhét tạo ra một siêu lớp (God class) chfía các Trường dữ liệu rỗng.

- Lớp phụ thuộc (Value Object): Address. Đại diện cho dữ liệu vị trí vật lý (giao hàng, thanh

toán), mang tính bất biến.

- Lớp phân quyền: Permission. Quản lý danh sách các đặc quyền truy cập tài nguyên chi tiết.
- Lớp trung gian: User_Permission (Đóng vai trò nối tham chiếu giữa User và

Permission).

### Bước 2: Xác định thuộc tính

- Lớp User
    - id: int (Primary Key)
    - username: string (Unique, Index để tối ưu tốc độ login)
    - password_hash: string (Tuyệt đối không lưu plain-text)
    - email: string
    - is_active: boolean (Sử dụng cơ chế soft-delete thay vì xóa cứng record để bảo toàn tính toàn vẹn dữ liệu lịch sử giao dịch)
- Lớp Customer (Kế thừa User)
    - loyalty_points: int (Điểm tích lũy)
    - customer_rank: string (Hạng thành viên: Standard, Silver, Gold)
- Lớp Staff (Kế thừa User)
    - employee_id: string (Mã nhân viên định danh nội bộ)
    - department: string (Phòng ban trực thuộc)
- Lớp Address
    - id: int

- - street: string
    - city: string
    - zip_code: string
- Lớp Permission
    - id: int
    - action_code: string (VD: "CREATE_ORDER", "UPDATE_CATALOG")
- Lớp User_Permission
    - user_id: int (Foreign Key trỏ về primary key của bảng User).
    - permission_id: int (Foreign Key trỏ về primary key của bảng Permission).
    - granted_at: datetime (Lưu vết thời điểm cấp quyền, bắt buộc phải có để phục vụ luồng Audit/Traceability).
    - granted_by: int (ID của Admin đã thực hiện cấp quyền, đảm bảo tính tracking).

### Bước 3: Xác định quan hệ

- Inheritance (Generalization): Customer, Staff, Admin → User
    - Giải thích kỹ thuật: Mối quan hệ "is-a". Thay vì tạo một bảng User khổng lồ chfía các cột null (sparse table) cho nhưng thuộc tính mà Customer không có nhưng Staff lại cần, mô hình kế thừa cho phép bóc tách cấu trúc. Trong hệ quản trị CSDL quan hệ hoặc framework như Django, kiến trúc này được mapping bằng kỹ thuật Class Table Inheritance (mỗi lớp con một bảng, nối với nhau qua ID của bảng User gốc).
- Composition: User → Address
    - Ký hiệu: 1..1 → 0..\* (Hình thoi đặc bên phía User).
    - Giải thích kỹ thuật: Mối quan hệ vòng đời phụ thuộc chặt chẽ (has-parts). Thực thể Address không mang ý nghĩa nghiệp vụ nếu đứng độc lập. Nếu một tài khoản User bị hủy bỏ hoàn toàn khỏi hệ thống, toàn bộ dữ liệu Address liên đới phải bị xóa theo cơ chế Cascade Delete để chống rác dữ liệu. Mọi thao tác thêm/sửa/xóa địa chỉ bắt buộc phải định tuyến qua Aggregate Root là User.
- Association: User → User_Permission
    - Ký hiệu: 1..1 → 0..\*
    - Giải thích: Một người dùng (User) có thể sở hfiu không hoặc nhiều bản ghi phân quyền (User_Permission).
- Association: Permission → User_Permission
    - Ký hiệu: 1..1 → 0..\*
    - Giải thích: Một đặc quyền (Permission) có thể được cấp phát cho không hoặc nhiều bản ghi người dùng (User_Permission).

## Thiết kế Cart Service

### Bước 1: Xác định lớp (Classes)

Cart Context phân tách dữ liệu thành hai lớp cốt lõi để đảm bảo tính toàn vẹn của giao dịch:

- Lớp trung tâm (Aggregate Root): Cart. Thực thể này chịu trách nhiệm kiểm soát vòng đời của toàn bộ giỏ hàng được cấp phát cho một phiên (session) hoặc một người dùng cụ thể. Mọi thao tác tính toán tổng phụ (subtotal) hay cập nhật số lượng đều phải đi qua điểm nghẽn (entry point) này.
- Lớp thành phần (Entity): CartItem. Đại diện cho một mặt hàng cụ thể đang nằm trong giỏ.

Lớp này không tồn tại độc lập mà bị ràng buộc hoàn toàn vào Aggregate Root Cart.

### Bước 2: Xác định thuộc tính (Attributes)

Cấu trúc dữ liệu của Cart Service bị ép buộc phải cắt bỏ mọi Trường thông tin dff thừa nhằm tối ưu tốc độ ghi xuống cơ sở dữ liệu hoặc bộ nhớ đệm (như Redis).

- Lớp Cart
    - id: int (Primary Key)
    - user_id: int (Lưu ý thiết kế: Chỉ lưu định danh của Customer, tuyệt đối không tham chiếu trực tiếp đối tượng User để giữ mức độ phụ thuộc lỏng lẻo - loose coupling với User Service). Đối với khách vãng lai, Trường này có thể null và được thay thế bằng một chuỗi session_id băm từ cookie của trình duyệt.
    - created_at: datetime
    - updated_at: datetime (Đóng vai trò là cờ hiệu (flag) bắt buộc để hệ thống chạy các luồng batch job dọn dẹp, tự động xóa các giỏ hàng bị bỏ hoang sau một khoảng thời gian session timeout).
- Lớp CartItem
    - id: int (Primary Key)
    - cart_id: int (Foreign Key nội bộ trỏ về bảng Cart).
    - product_id: int (Chỉ lưu mã định danh sản phẩm. Thiết kế này cắt đfít hoàn toàn khóa ngoại vật lý sang database của Product Service).
    - quantity: int (Ràng buộc logic: phải lớn hơn 0).
    - _(Lưu ý kỹ thuật: Thuộc tính price không được lưu cứng tại đây. Giá sản phẩm có thể biến động liên tục từ phía Product Service, do đó Cart Service chỉ lưu quantity và buộc phải gọi API ra ngoài để tính toán thành tiền theo thời gian thực)._

### Bước 3: Xác định quan hệ (Relationships)

- Composition: Cart → CartItem
    - Ký hiệu: 1..1 → 0..\* (Hình thoi đặc đặt bên phía Cart).
    - Giải thích kỹ thuật: Đây là quan hệ phụ thuộc vòng đời sống còn (has-parts). Một CartItem không mang bất kỳ ý nghĩa nghiệp vụ nào nếu nó bị tách rời khỏi Cart. Khi hệ thống thực thi lệnh xóa một giỏ hàng (do khách hàng chốt đơn thành công chuyển sang Order, hoặc do timeout), toàn bộ các CartItem bên trong bắt buộc phải bị hủy diệt theo cơ chế Cascade Delete để giải phóng tài nguyên.

- Association (Logical): CartItem → Product
    - Ký hiệu: 0..\* → 1..1
    - Giải thích kỹ thuật: Một mặt hàng trong giỏ chỉ trỏ đến đúng một sản phẩm. Tuy nhiên, vì hai thực thể này bị chia cắt bởi ranh giới mạng của hai microservices, kết nối này chỉ là liên kết logic thông qua product_id. Khi giao diện cần hiển thị hình ảnh và giá sản phẩm, hệ thống bắt buộc phải áp dụng mẫu thiết kế API Composition, sử dụng API Gateway để gọi đồng thời Cart Service và Product Service rồi mới gộp dữ liệu.
- Association (Logical): Cart → User
    - Ký hiệu: 0..\* → 1..1
    - Giải thích kỹ thuật: Mối quan hệ tham chiếu lỏng. Một User có thể tạo ra nhiều Cart qua các thời điểm khác nhau, nhưng một Cart tại một thời điểm chỉ thuộc về duy nhất một User. Mối quan hệ này cũng chỉ được duy trì bằng user_id để ngăn chặn việc khóa bảng chéo hệ thống.

## Thiết kế Order Service

### Bước 1: Xác định lớp (Classes)

Dưới góc độ Domain-Driven Design (DDD), miền Order khoanh vùng các lớp dữ liệu trực tiếp định hình giao dịch tài chính và luồng luân chuyển hàng hóa.

- Lớp trung tâm (Aggregate Root): Order. Thực thể nòng cốt kiểm soát vòng đời đơn hàng, đóng vai trò điểm nghẽn truy xuất (entry point). Mọi thao tác tính toán tổng tiền, cập nhật trạng thái hay áp mã giảm giá đều phải đi qua lớp này để đảm bảo tính nhất quán (data consistency).
- Lớp thành phần (Entity): OrderItem. Đại diện cho các mặt hàng trong đơn. Không tồn tại

độc lập ngoài ngữ cảnh của Order.

- Lớp phụ thuộc (Value Object): DeliveryInfo và PaymentInfo. Nhóm các Trường dữ liệu liên quan đến vận chuyển và thanh toán, giúp giảm thiểu hiện tượng "siêu lớp" (God class) phình to cho Order.
- Lớp khuyến mãi: Voucher và OrderDiscount. Quản lý quy tắc giảm giá tĩnh và vết lưu trữ

mã giảm giá đã áp dụng cho từng đơn hàng cụ thể.

### Bước 2: Xác định thuộc tính (Attributes)

Cấu trúc thuộc tính cắt đfít mọi khóa ngoại (Foreign Keys) vật lý tới User Service hay Product Service để duy trì tính tự trị. Dữ liệu giá bán phải được lưu cứng ngay tại thời điểm chốt đơn nhằm chặn đứng nguy cơ sai lệch lịch sử giao dịch nếu Product Service cập nhật giá sau này.

- Lớp Order
    - id: int (Primary Key)
    - customer_id: int (Định danh logic, không tham chiếu trực tiếp đối tượng User).

- - status: string (Sử dụng cờ trạng thái như APPROVAL_PENDING, APPROVED, SHIPPED, CANCELLED làm khóa ngữ nghĩa - semantic lock - để cô lập giao dịch trong luồng Saga).
    - subtotal: float (Tổng tiền hàng gốc).
    - discount_amount: float (Số tiền được trữ từ logic khuyến mãi tính toán nội bộ).
    - total_price: float (Số tiền cuối cùng chuyển sang Payment Service).
    - created_at: datetime
- Lớp OrderItem
    - id: int
    - order_id: int (Khóa ngoại nội bộ trỏ về bảng Order).
    - product_id: int (Tham chiếu logic sang Product Service).
    - quantity: int
    - price: float (Giá tại thời điểm mua, sao chép bất biến từ Product Service).
- Lớp DeliveryInfo
    - address: string
    - shipping_method: string
    - tracking_number: string
- Lớp PaymentInfo
    - transaction_id: string (Lưu vết từ cổng thanh toán bên thứ ba).
    - payment_method: string
- Lớp Voucher
    - code: string (Primary Key)
    - discount_percent: float
    - max_discount_amount: float
    - min_order_value: float (Điều kiện biên để áp dụng luật khuyến mãi).
    - is_active: boolean
- Lớp OrderDiscount
    - id: int
    - order_id: int
    - voucher_code: string

### Bước 3: Xác định quan hệ (Relationships)

- Composition: Order → OrderItem
    - Ký hiệu: 1..1 → 1..\* (Hình thoi đặc bên phía Order).
    - Giải thích kỹ thuật: Quan hệ phụ thuộc vòng đời (has-parts). Một OrderItem không mang ý nghĩa nếu đứng độc lập. Khi một Order bị xóa (hoặc rollback do lỗi thanh toán), toàn bộ OrderItem bên trong bắt buộc phải bị hủy diệt theo cơ chế Cascade Delete để bảo vệ tính toàn vẹn dữ liệu.
- Composition: Order → DeliveryInfo, PaymentInfo
    - Ký hiệu: 1..1 → 1..1 (Hình thoi đặc bên phía Order).

- - Giải thích kỹ thuật: Mặc dù tách lớp để hướng đối tượng, các luồng thông tin này vẫn bám chặt vào vòng đời của một giao dịch đơn hàng. Ở tầng CSDL quan hệ, các lớp này có thể được gộp phẳng (flatten) trực tiếp vào bảng orders (như @Embedded trong JPA) để giảm chi phí lệnh SQL JOIN nội bộ.
- Association: Order → Voucher
    - Ký hiệu: 0..\* → 0..1.
    - Giải thích kỹ thuật: Một đơn hàng có thể áp dụng tối đa một mã khuyến mãi, trong khi một mã khuyến mãi có thể được tái sử dụng cho nhiều đơn hàng hợp lệ.
- Composition: Order → OrderDiscount
    - Ký hiệu: 1..1 → 0..\* (Hình thoi đặc bên phía Order).
    - Giải thích kỹ thuật: Mối quan hệ phụ thuộc vòng đời (has-parts). OrderDiscount sinh ra để lưu vết chính xác mã giảm giá nào đã được áp dụng và số tiền được trữ đi trên một đơn hàng cụ thể. Thực thể này hoàn toàn vô nghĩa nếu đứng độc lập. Khi một Order bị hủy bỏ (xóa vật lý) hoặc rollback do giao dịch lỗi, toàn bộ các bản ghi OrderDiscount liên đới bắt buộc phải bị tiêu diệt theo cơ chế Cascade Delete để ngăn chặn rác dữ liệu.
- Association: OrderDiscount → Voucher
    - Ký hiệu: 0..\* → 1..1.
    - Giải thích kỹ thuật: Ở cấp độ cơ sở dữ liệu, OrderDiscount đóng vai trò là một lớp trung gian (associative entity) giải quyết bài toán quan hệ n-n giữa Đơn hàng và Khuyến mãi. Thay vì nhồi nhét trực tiếp voucher_code vào bảng Order (gây giới hạn nếu hệ thống cho phép áp dụng đồng thời mã Freeship và mã giảm giá shop), thiết kế tách rời này mang lại khả năng mở rộng tốt hơn. Một mã Voucher tĩnh có thể được hàng ngàn khách hàng sử dụng, sinh ra hàng ngàn bản ghi OrderDiscount khác nhau. Tuy nhiên, mỗi OrderDiscount chỉ trỏ ngược về đúng một Voucher gốc. Việc thiết lập liên kết này là nền tảng kỹ thuật bắt buộc để hệ thống đếm tổng số lffợt đã sử dụng của một mã ưu đãi, từ đó kích hoạt logic chặn áp mã nếu vffợt quá giới hạn ngân sách (max_uses).
- Association (Logical): Order → Customer (User Context)
    - Ký hiệu: 0..\* → 1..1.
    - Giải thích kỹ thuật: Quan hệ tham chiếu xuyên miền. Database của Order Service chỉ lưu customer_id. Nếu giao diện cần hiển thị tên khách hàng trên hóa đơn, hệ thống bắt buộc sử dụng API Gateway để gọi API Composition ghép nối dữ liệu hoặc sử dụng CQRS, tuyệt đối cấm dùng khóa ngoại vật lý (Foreign Key) trỏ chéo làm sập đặc tính triển khai độc lập.
- Association (Logical): OrderItem → Product (Product Context)
    - Ký hiệu: 0..\* → 1..1.
    - Giải thích kỹ thuật: Giống Customer, OrderItem chỉ giữ product_id làm cầu nối định tuyến sang service Sản phẩm.

## Thiết kế Payment Service

### Bước 1: Xác định lớp (Classes)

Tuân thủ nguyên tắc Domain-Driven Design (DDD), Payment Context không được phép ôm đồm các cấu trúc dữ liệu của đơn hàng hay người dùng. Các lớp được giới hạn nghiêm ngặt trong phạm vi theo dõi dòng tiền:

- Lớp trung tâm (Aggregate Root): Payment. Thực thể nòng cốt kiểm soát vòng đời của một phiên thanh toán. Mọi thao tác cập nhật số dff hay thay đổi trạng thái giao dịch đều bắt buộc phải đi qua điểm nghẽn này nhằm đảm bảo tính nhất quán dữ liệu nội bộ.
- Lớp thành phần (Entity): TransactionLog. Lưu vết (audit) toàn bộ lịch sử gfíi/nhận request

với cổng thanh toán bên thứ ba. Lớp này đóng vai trò sống còn để hệ thống thực thi đối soát (reconciliation) hoặc xử lý luồng hoàn tiền (refund) khi có khiếu nại.

- Lớp phụ thuộc (Value Object / Entity): PaymentMethod. Đại diện cho kênh thanh toán mà

khách hàng lựa chọn, chfía các cấu hình đặc thù để định tuyến request sang đúng nhà cung cấp dịch vụ.

### Bước 2: Xác định thuộc tính (Attributes)

Cấu trúc bảng dữ liệu của Payment Service buộc phải lưu cứng order_id dưới dạng tham chiếu logic, đồng thời sao chép chính xác số tiền cần thanh toán. Việc này chặn đứng nguy cơ giao dịch bị sai lệch số liệu nếu Product Service hoặc Order Service thay đổi thông tin sau thời điểm chốt đơn.

- Lớp Payment
    - id: int (Primary Key)
    - order_id: int (Định danh logic trỏ về Order Service, tuyệt đối cấm Foreign Key vật lý).
    - amount: float (Số tiền giao dịch thực tế).
    - currency: string (Mã tiền tệ, VD: 'VND', 'USD').
    - status: string (Sử dụng các cờ trạng thái: PENDING, SUCCESS, FAILED, REFUNDED

làm khóa ngữ nghĩa cho tiến trình).

- - created_at: datetime
- Lớp TransactionLog
    - id: int (Primary Key)
    - payment_id: int (Khóa ngoại nội bộ trỏ về bảng Payment).
    - gateway_transaction_id: string (Mã giao dịch định danh trả về từ cổng 3rd-party, dùng để gỡ lỗi và đối soát chéo).
    - response_code: string (Mã phản hồi HTTP hoặc mã lỗi nghiệp vụ từ cổng thanh toán).
- Lớp PaymentMethod
    - id: int (Primary Key)
    - name: string (VD: 'Credit Card', 'PayPal', 'COD').
    - provider: string (Định danh API provider xử lý trung gian).

### Bước 3: Xác định quan hệ (Relationships)

Mạng lffới quan hệ bên trong Payment Service ưu tiên tính khép kín vật lý. Bất kỳ tham chiếu nào vắt ngang ranh giới domain đều bị giáng cấp xuống mức liên kết ID nhằm đảm bảo tính tự trị dữ liệu.

- Composition: Payment → TransactionLog
    - Ký hiệu: 1..1 → 1..\* (Hình thoi đặc đặt bên phía Payment).
    - Giải thích kỹ thuật: Mối quan hệ phụ thuộc vòng đời sống còn (has-parts). Một bản ghi TransactionLog sinh ra để lưu vết cho một lần gọi API của một Payment cụ thể; nó hoàn toàn vô nghĩa nếu đứng độc lập. Khi một Payment bị xóa khỏi hệ thống, toàn bộ log giao dịch liên đới bắt buộc phải bị tiêu diệt theo cơ chế Cascade Delete ở cấp độ cơ sở dữ liệu để dọn rác bộ nhớ.
- Association: Payment → PaymentMethod
    - Ký hiệu: 0..\* → 1..1

- - Giải thích kỹ thuật: Nhiều phiên thanh toán có thể sử dụng chung một phffơng thức (VD: hàng ngàn user chọn thanh toán bằng thẻ Visa). Liên kết này giúp hệ thống phân cụm dòng tiền theo từng kênh để tạo báo cáo doanh thu tài chính.
- Association (Logical): Payment → Order (Order Context)
    - Ký hiệu: 0..\* → 1..1
    - Giải thích kỹ thuật: Quan hệ tham chiếu chéo mạng (Cross-boundary reference). Khi cổng thanh toán trả về kết quả và Payment chuyển trạng thái sang SUCCESS, Payment Service không được phép dùng lệnh SQL UPDATE trực tiếp sang bảng dữ liệu của Order. Thay vào đó, nó đóng vai trò là một nhà xuất bản (Publisher), phát đi một sự kiện PaymentCompletedEvent vào Message Broker (như Kafka/RabbitMQ). Order Service sẽ lắng nghe sự kiện này để tự động cập nhật trạng thái đơn hàng của nó. Mặc dù thiết kế hướng sự kiện này phát sinh chi phí vận hành Message Broker, nó bẻ gãy hoàn toàn sự phụ thuộc đồng bộ, loại bỏ rủi ro khóa bảng chéo (cross-database locks) làm nghẽn hệ thống.

## Thiết kế Shipping Service

### Bước 1: Xác định lớp (Classes)

- Lớp trung tâm (Aggregate Root): Shipment. Quản lý toàn bộ vòng đời luân chuyển vật lý của một gói hàng. Đây là điểm nghẽn truy xuất bắt buộc; mọi thao tác cập nhật vị trí hay thay đổi trạng thái giao nhận đều phải đi qua thực thể này.
- Lớp thành phần (Entity): Courier. Quản lý thông tin định danh, vị trí và trạng thái khả

dụng của đối tác giao hàng.

- Lớp lưu vết (Entity): ShippingTracking. Ghi nhận các mốc lịch sử di chuyển của gói hàng theo thời gian thực phục vụ truy xuất lộ trình.

### Bước 2: Xác định thuộc tính (Attributes)

- Lớp Shipment
    - id: int (Primary Key)
    - order_id: int (Định danh tham chiếu logic sang Order Service. Tuyệt đối không thiết lập khóa ngoại vật lý để duy trì tính tự trị dữ liệu).
    - address: string (Địa chỉ giao hàng. Bắt buộc sao chép cứng dữ liệu từ Order Service tại thời điểm tạo đơn, chặn đứng rủi ro sai lệch lịch sử nếu khách hàng đổi địa chỉ trong profile sau này).
    - status: string (Sử dụng khóa ngữ nghĩa nội bộ: PROCESSING, SHIPPING, DELIVERED).
- Lớp Courier
    - id: int (Primary Key)
    - name: string
    - phone: string
    - current_location: string (Lưu tọa độ vĩ độ/kinh độ để theo dõi theo thời gian thực).
    - is_available: boolean (Cờ trạng thái quyết định việc tài xế có thể tiếp nhận thêm đơn hay không).
- Lớp ShippingTracking
    - id: int
    - shipment_id: int (Khóa ngoại nội bộ trỏ về bảng Shipment).
    - checkpoint: string (Mô tả vị trí vật lý, VD: "Rời kho trung chuyển", "Đang giao").
    - timestamp: datetime

### Bước 3: Xác định quan hệ (Relationships)

- Composition: Shipment → ShippingTracking
    - Ký hiệu: 1..1 → 0..\* (Hình thoi đặc bên phía Shipment).
    - Giải thích kỹ thuật: Mối quan hệ phụ thuộc vòng đời sống còn (has-parts). Bản ghi ShippingTracking sinh ra chỉ để phục vụ luồng log di chuyển của một Shipment cụ thể. Nếu bản ghi Shipment bị hủy bỏ (do khách hủy đơn từ hệ thống trước khi xuất kho), toàn bộ log di chuyển liên đới bắt buộc phải bị tiêu diệt bằng cơ chế Cascade Delete dưới cơ sở dữ liệu để giải phóng tài nguyên bộ nhớ.
- Association: Courier → Shipment

- - Ký hiệu: 0..1 → 0..\*
    - Giải thích kỹ thuật: Một tài xế (Courier) có thể tiếp nhận nhiều gói hàng (Shipment) cùng tuyến, nhưng mỗi gói hàng tại một thời điểm chỉ được gán cho duy nhất một người giao. Liên kết này mang tính linh hoạt, cho phép hệ thống thực thi thuật toán gán lại (re-assign) mã courier_id trên bảng Shipment nếu tài xế gặp sự cố giữa đffờng.
- Association (Logical): Shipment → Order (Order Context)
    - Ký hiệu: 0..\* → 1..1
    - Giải thích kỹ thuật: Mối quan hệ tham chiếu chéo mạng (Cross-boundary reference). Database của Shipping Service chỉ nắm giữ order_id. Khi tài xế xác nhận giao hàng thành công và Shipment chuyển sang trạng thái DELIVERED, tiến trình này không được phép thực thi câu lệnh SQL UPDATE chéo mạng sang database của Order Service. Thay vào đó, Shipping Service hoạt động như một nhà xuất bản, đẩy sự kiện DeliveryDelivered vào Message Broker. Order Service đóng vai trò hạ nguồn (downstream) lắng nghe sự kiện này để tự động cập nhật trạng thái hoàn thành đơn. Mặc dù kiến trúc hướng sự kiện (Event-Driven) này phát sinh chi phí vận hành Message Broker, nó loại bỏ hoàn toàn rủi ro khóa bảng (database locks) chéo làm nghẽn luồng xử lý đồng bộ.

## Luồng hệ thống tổng thể

**Bước 1 và 2: Xác thực và Duyệt sản phẩm (User & Product)** Mọi request từ client bắt buộc phải đi qua màng lọc API Gateway. Tại đây, token JWT được bóc tách và chuyển tới User Service để xác thực danh tính phi trạng thái. Khi quyền truy cập được phê duyệt, luồng đọc (read-heavy) định tuyến thẳng đến Product Service. Thao tác truy vấn danh mục bỏ qua hoàn toàn các lệnh SQL JOIN đến bảng người dùng, giúp Product Service tự do mở rộng (scale) để chống chịu lưu lượng truy cập lớn trong các đợt Flash Sale mà không gây nghẽn cổ chai ở tầng database.

**Bước 3: Lưu trữ tạm thời (Cart)** Khi người dùng chọn món hàng, API Gateway đẩy lệnh ghi xuống Cart Service. Vì giỏ hàng có tần suất I/O cực cao nhưng vòng đời ngắn, dịch vụ này chỉ lưu trữ định danh nguyên thủy (user_id và product_id) trên bộ nhớ đệm. Việc cắt đfít khóa ngoại vật lý sang cơ sở dữ liệu của Product Service triệt tiêu hoàn toàn độ phụ thuộc tĩnh, bảo vệ tiến trình mua sắm không bị gián đoạn ngay cả khi Product Service tạm thời ngắt kết nối.

**Bước 4: Điều phối giao dịch phân tán (Order)** Điểm bùng nổ độ phức tạp hệ thống nằm ở thao tác chốt đơn. Khi request POST chạm đến Order Service, dịch vụ này đảm nhận vai trò điều phối trung tâm (Orchestrator). Nó gọi đồng bộ (REST/gRPC) sang Cart Service để lấy danh sách món hàng và Product Service để chốt giá. Tại khoảnh khắc này, ranh giới ACID toàn cục chính thức bị phá vỡ. Thay vì sử dụng giao thức 2PC làm khóa chết toàn bộ hệ thống, Order Service áp dụng mẫu thiết kế Saga. Nó ghi nhận bản ghi đơn hàng ở trạng thái PENDING vào database cục bộ, sau đó lập tfíc trả về mã HTTP 200 cho client để giải phóng luồng, đẩy phần xử lý nặng nề còn lại xuống nền background.

**Bước 5 và 6: Xử lý thanh toán và Kích hoạt giao hàng (Payment & Shipping)** Luồng thực thi tiếp tục bẻ nhánh sang giao tiếp bất đồng bộ (Event-Driven). Order Service gfíi lệnh trữ tiền đến Payment Service. Dịch vụ thanh toán xử lý với cổng bên thứ 3 và tự giam lỏng mọi lỗi timeout ở không gian của nó để bảo vệ hệ thống lõi. Khi giao dịch tài chính hoàn tất, thay vì gọi API đồng bộ để cập nhật bảng dữ liệu chéo, Payment Service đóng vai trò nhà xuất bản (Publisher), phát đi một sự kiện PaymentCompletedEvent vào Message Broker.

Đầu ra của sự kiện này thiết lập luồng xử lý song song:

1.  Order Service (đóng vai trò Subscriber) bắt được sự kiện, tự động cập nhật trạng thái đơn hàng từ PENDING sang APPROVED.
2.  Shipping Service đồng thời tiêu thụ sự kiện này để sinh ra bản ghi Shipment, phân rã hoàn toàn logic điều phối tài xế ra khỏi vòng đời của hóa đơn tài chính.

Kiến trúc luồng tổng thể bóc tách rõ ràng hai pha vận hành: mặt ngoài đồng bộ để phản hồi client tfíc thì, mặt trong bất đồng bộ để duy trì hệ sinh thái lỏng lẻo. Thiết kế này ép buộc hệ thống phải đánh đổi tính nhất quán tfíc thời để đổi lấy tính sẵn sàng cao và khả năng cô lập lỗi tuyệt đối giữa các tiến trình

## Kết luận

Việc xé nhỏ hệ thống E-Commerce thành các tiến trình độc lập không phải là phffơng án hoàn hảo tuyệt đối, mà là một sự đánh đổi hạ tầng. Để đổi lấy khả năng co giãn độc lập tại các điểm nghẽn và duy trì tính sẵn sàng cao, kiến trúc Microservices ép buộc hệ thống phải gánh chịu trực tiếp độ trễ mạng và đối mặt với bài toán nhất quán dữ liệu phân tán phức tạp.

Domain-Driven Design (DDD) đóng vai trò là cơ sở lý thuyết sống còn giúp thiết kế đúng ngay từ đầu. Nếu thiếu đi ranh giới Bounded Context cứng rắn, hệ thống sẽ lập tfíc thoái hóa thành một mớ nguyên khối phân tán. Việc băm nhỏ database, cấm tuyệt đối lệnh SQL JOIN chéo mạng và bắt buộc giao tiếp thông qua hợp đồng API (API contracts) đã thiết lập được tính tự trị cho từng service. Thiết kế này chặn đứng rủi ro khóa bảng chéo, bảo vệ luồng giao dịch cốt lõi khỏi hiệu ứng sụp đổ dây chuyền.

Dưới góc độ cài đặt vật lý, việc lựa chọn framework Django đóng vai trò bệ phóng giúp tăng tốc độ triển khai ứng dụng. Mặc dù bản chất Django sinh ra để phục vụ mô hình Monolithic, nhưng khi kết hợp với Django REST Framework (DRF) và quy hoạch mã nguồn tuân thủ nghiêm ngặt ranh giới domain, nó hoàn toàn đáp ứng được việc bọc gói các RESTful API. Tuy nhiên, kỹ sư buộc phải can thiệp sâu để vô hiệu hóa các ràng buộc khóa ngoại được hỗ trợ sẵn bởi Django ORM xuyên qua các app, nhằm đảm bảo sự cô lập dữ liệu tuyệt đối giữa các tiến trình microservices.

Một hệ thống E-commerce giao dịch thuần túy (CRUD) chỉ là tầng móng hạ tầng. Lượng dữ liệu hành vi (behavior data) khổng lồ sinh ra từ mạng lffới microservices này mới là tài sản cốt lõi. Chffơng tiếp theo sẽ chuyển hướng sang AI Service, tập trung giải quyết bài toán biến luồng dữ liệu thô này thành các mô hình gợi ý sản phẩm (Recommendation System) và Chatbot tư vấn, từ đó trực tiếp thúc đẩy tỷ lệ chuyển đổi đơn hàng.

# CHƯƠNG 3: AI SERVICE CHO TƯ VẤN SẢN PHẨM

## Mục tiêu

Việc thiết lập một AI Service độc lập trong hệ thống E-commerce nhằm giải quyết ranh giới giới hạn của các truy vấn SQL truyền thống khi đối mặt với dữ liệu hành vi phi cấu trúc và ý định mua sắm mờ của khách hàng. Mục tiêu kỹ thuật cốt lõi của phân hệ này được định hình dựa trên ba trụ cột xử lý dữ liệu và hai hợp đồng đầu ra tiêu chuẩn.

- _Thứ nhất, dự đoán hành vi qua mô hình chuỗi._ AI Service phải tiêu thụ luồng dữ liệu tương tác thô theo thời gian thực (view, click, add-to-cart, ...) để phác họa chính xác luồng hành vi mua sắm,. Mục tiêu ở đây không dững lại ở việc tính toán tỷ lệ nhấp chuột ngắn hạn. Thay vào đó, hệ thống buộc phải dự đoán được sản phẩm mục tiêu tiếp theo người dùng muốn hướng tới, từ đó giải quyết bài toán tối ưu hóa tỷ lệ chuyển đổi và tăng mức độ hài lòng dài hạn của khách hàng.
- _Thứ hai, khai thác độ phụ thuộc dữ liệu qua mạng lưới đồ thị._ Mặc dù các thuật toán lọc

cộng tác giải quyết tốt bài toán gợi ý chung, chúng lại sinh ra điểm mù "khởi động lạnh" (cold-start) đối với người dùng vãng lai hoặc mặt hàng mới lên kệ,. Để khắc phục sự đánh đổi này, AI Service đặt mục tiêu ánh xạ các thực thể (User, Product) thành một Knowledge Graph. Hệ thống phải định lượng được mối quan hệ tương đồng và tính liên kết chéo giữa các tập sản phẩm dựa trên thuộc tính tập hợp, thay vì phụ thuộc hoàn toàn vào số lượng giao dịch trong quá khfí,.

- _Thứ ba, cá nhân hóa tương tác dựa trên ngữ cảnh._ Đối với luồng giao tiếp trực tiếp, dịch

vụ phải bọc gói khả năng xử lý ngôn ngữ tự nhiên thông qua một Chatbot tư vấn, với mục tiêu hiểu chính xác ngữ cảnh truy vấn thay vì chỉ khớp từ khóa. Đặc biệt, để triệt tiêu rủi ro mô hình ngôn ngữ lớn (LLM) sinh ra thông tin ảo như tư vấn sai giá hoặc sai thông số cấu hình, hệ thống buộc phải tích hợp kỹ thuật truy xuất tăng cffờng (RAG) nhằm neo chặt câu trả lời vào vùng cơ sở dữ liệu sản phẩm nội bộ,.

- _Cuối cùng, chuẩn hóa đầu ra tích hợp._ Dưới góc độ kiến trúc, AI Service hoạt động như

một nhà cung cấp dữ liệu độc lập. Để các service hạ nguồn (như Cart hay Search) có thể tiêu thụ dữ liệu mà không bị dính chặt vào logic của AI, mục tiêu đầu ra được thiết lập cứng thành hai định dạng phản hồi: (1) Trả về một mảng định danh (list of IDs) các sản phẩm đề xuất cho giao diện tìm kiếm hoặc giỏ hàng; (2) Trả về chuỗi văn bản tự nhiên (text response) phục vụ cho giao diện Chatbot

## Kiến trúc AI service

Dưới góc độ thiết kế phân tán, AI Service được định tuyến vật lý thành một microservice hoàn toàn độc lập, tách rời khỏi các miền giao dịch cốt lõi của hệ thống E-commerce. Việc cô lập AI Service thiết lập một màng lọc chịu lỗi cứng rắn; dù khối lượng phân tích dữ liệu có gây quá tải cục bộ tại AI Service, luồng mua sắm và thanh toán của khách hàng vẫn sống sót.

Về luồng dữ liệu, kiến trúc nội bộ của AI Service vận hành dựa trên một pipeline xử lý khép kín gồm ba màng lọc: Input, Processing và Output.

- _Thứ nhất, luồng tiếp nhận (Input)._ Dịch vụ này đóng vai trò như một điểm hứng dữ liệu, liên tục hấp thụ hai luồng thông tin đầu vào:
    - (1) Dữ liệu hành vi nguyên thủy (User Behavior Data) như view, click, add_to_cart đi kèm các định danh (user_id, product_id) và dấu thời gian (timestamp);
    - (2) Các truy vấn ngôn ngữ tự nhiên được đẩy trực tiếp từ giao diện của người dùng.
- _Thứ hai, lõi xử lý (Processing)._ Thay vì dồn ép xử lý vào một thuật toán nguyên khối, kiến trúc phân rã logic tính toán cho ba công cụ chuyên biệt để giải quyết các bài toán khác nhau:
    - Mô hình chuỗi (LSTM): Gánh vác tác vụ mô hình hóa chuỗi thời gian (Sequence Modeling). Nó tiêu thụ luồng log hành vi để dò tìm quy luật và dự đoán xác suất sản phẩm tiếp theo mà người dùng sẽ click.
    - Đồ thị tri thức (Knowledge Graph): Triển khai bằng Neo4j, khối này làm nhiệm vụ bóc tách các mối quan hệ phức tạp mà mô hình chuỗi không nhìn thấy được. Các node (User, Product) được nối bằng các edge (BUY, VIEW, SIMILAR) để tạo ra mạng lffới gợi ý có tính tương đồng cao.
    - Bộ máy truy xuất tăng cffờng (RAG): Đảm nhiệm luồng xử lý truy vấn văn bản. Bằng cách nhúng dữ liệu vào Vector Database, RAG ép các mô hình ngôn ngữ lớn (LLM) phải sinh câu trả lời bám sát vào kho dữ liệu sản phẩm có thật, chặn đứng rủi ro chatbot bịa thông tin.
- _Cuối cùng, hợp đồng đầu ra (Output)._ Để bảo vệ tính phụ thuộc lỏng lẻo của hệ thống, AI

Service tuyệt đối không can thiệp vào cách giao diện hiển thị. Hợp đồng API của nó được thiết lập tĩnh thành hai định dạng: (1) Trả về một mảng chfía định danh các sản phẩm đề xuất (dành cho tính năng gợi ý Recommendation); (2) Trả về trực tiếp chuỗi văn bản (dành cho Chatbot phản hồi).

## Thu thập dữ liệuUser Behavior Data

Cấu trúc cốt lõi của một bản ghi dữ liệu hành vi được thiết kế tinh gọn với 4 Trường thông tin:

- - - - user_id: Định danh người dùng để ghim vết hành vi. Đây là tham chiếu logic trỏ về User Service thay vì khóa ngoại vật lý, giúp AI Service tách biệt khỏi tầng dữ liệu nguyên khối.
            - product_id: Mã định danh sản phẩm được tương tác, đóng vai trò ánh xạ sang kho dữ liệu

của Product Service để lấy thông tin chi tiết khi đffa vào huấn luyện.

- - - - action: Phân loại hành vi tương tác, được giới hạn trong tập giá trị tĩnh. Sự phân lớp này giúp thuật toán gán trọng số ý định (intent weighting); tín hiệu add_to_cart có tần suất sinh ra thấp nhưng mang hàm lượng ý định chốt đơn cao hơn hẳn so với lượng lớn nhiễu (noise) từ thao tác view.
                - 1\. view (Xem lffớt danh sách): Tần suất sinh ra lớn nhất, tỷ lệ nhiễu (noise) cao nhất. Dù tốn dung lượng lưu trữ, luồng dữ liệu này bắt buộc phải có để khởi tạo các trạng thái ẩn ban đầu cho mô hình LSTM, giúp AI biết khách hàng đã lffớt qua nhưng gì trước khi tương tác.

- - - - - 2\. click (Nhấn xem chi tiết): Xác nhận sự chú ý có chủ đích. Mỗi sự kiện click sẽ trực tiếp sinh ra một cạnh (edge) liên kết giữa node User và node Product bên trong Knowledge Graph (Neo4j), làm nền tảng cho các thuật toán dò tìm đffờng đi.
                - 3\. search (Tìm kiếm): Hành vi mang ý định chủ động rõ ràng nhất. Lịch sử text từ search được vector hóa (embedding) thông qua mô hình ngôn ngữ lớn để phục vụ cho các truy vấn của Chatbot RAG, hạn chế tình trạng bot tư vấn sai nhu cầu.
                - 4\. add_to_wishlist (Thêm vào yêu thích): Tín hiệu định hình sở thích dài hạn. Khác với giỏ hàng có vòng đời ngắn, wishlist giúp AI bảo toàn được lịch sử dự đoán ngay cả khi người dùng đăng xuất và quay lại sau nhiều tháng.
                - 5\. add_to_cart (Thêm vào giỏ): Tín hiệu mang ý định chuyển đổi ngắn hạn cực mạnh. Trong Bước cấu hình hàm mất mát (loss function) của neural network, hành vi này phải được gán trọng số (weight) cao hơn hẳn view hay click.
                - 6\. remove_from_cart (Xóa khỏi giỏ hàng): Phản hồi âm sống còn. Nếu bỏ qua event này, AI sẽ liên tục gợi ý lại nhưng món hàng khách đã loại bỏ. Việc tracking remove giúp mô hình lập tfíc bắt được sự dịch chuyển ý định theo thời gian thực.
                - 7\. purchase (Thanh toán thành công): Ground truth tuyệt đối của mô hình. Đây là nhãn cuối cùng được dùng để đo lffờng tỷ lệ chính xác của các thuật toán phân tích (Recommendation System).
                - 8\. rate_review (Đánh giá/Chấm điểm): Tín hiệu xác nhận sự hài lòng sau giao dịch. Một lffợt mua nhưng đánh giá 1 sao sẽ kích hoạt cơ chế trữ điểm tương đồng trên đồ thị, ngăn AI gợi ý sản phẩm lỗi đó cho các user có chung hành vi.
            - timestamp: Dấu thời gian ghi nhận sự kiện. Trường dữ liệu này mang tính sống còn đối

với mô hình Sequence Modeling như LSTM. Thuật toán phân tích chuỗi bắt buộc phải dựa vào thứ tự thời gian tuyến tính để bóc tách chính xác Bước dịch chuyển trong hành trình mua sắm của người dùng.

## Ví dụ dataset

|     |     |     |     |
| --- | --- | --- | --- |
| **user_id** | **product_id** | **action** | **timestamp** |
| 326 | 89  | view | 1/27/2026 15:57 |
| 326 | 89  | click | 1/27/2026 16:00 |
| 326 | 89  | add_to_cart | 1/27/2026 16:02 |
| 326 | 89  | purchase | 1/27/2026 16:06 |
| 326 | 79  | view | 1/27/2026 16:06 |
| 326 | 79  | click | 1/27/2026 16:10 |
| 326 | 80  | view | 1/27/2026 16:12 |
| 326 | 80  | click | 1/27/2026 16:16 |
| 326 | 84  | search | 1/27/2026 16:18 |
| 326 | 84  | view | 1/27/2026 16:20 |
| 326 | 84  | click | 1/27/2026 16:24 |
| 326 | 84  | add_to_cart | 1/27/2026 16:26 |
| 326 | 84  | purchase | 1/27/2026 16:31 |
| 456 | 134 | search | 1/27/2026 18:54 |
| 456 | 134 | view | 1/27/2026 18:55 |
| 456 | 134 | click | 1/27/2026 19:00 |

|     |     |     |     |
| --- | --- | --- | --- |
| 456 | 134 | add_to_cart | 1/27/2026 19:01 |
| 456 | 134 | purchase | 1/27/2026 19:02 |
| 125 | 19  | search | 1/28/2026 6:55 |
| 125 | 19  | view | 1/28/2026 6:57 |

## Mô hình LSTM (Sequence Modeling)Ý tưởng

Các thuật toán Lọc cộng tác truyền thống bộc lộ điểm yếu chí mạng khi triển khai trên hệ thống E-commerce thực tế: chúng chỉ phân tích ma trận tương tác tĩnh và bỏ qua hoàn toàn yếu tố chuỗi thời gian. Khi người dùng lffớt web, thứ tự của các cú click không phải là ngẫu nhiên; chúng mang ý nghĩa định hình trực tiếp sự dịch chuyển trong ý định mua sắm.

Mặc dù các mô hình dựa trên chuỗi Markov giải quyết được bài toán thứ tự bằng cách dự đoán hành vi tiếp theo dựa trên hành vi liền kề trước đó, kiến trúc này lại bị trói buộc bởi giả định độc lập quá cứng nhắc,. Hệ quả kỹ thuật là mô hình Markov chỉ "nhớ" được duy nhất thao tác cuối cùng, dẫn đến việc đánh mất toàn bộ ngữ cảnh của chuỗi hành vi phức tạp từ đầu phiên truy cập.

Để khắc phục triệt để điểm mù này, việc sử dụng mạng nơ-ron hồi quy (RNN) — cụ thể là mô hình Bộ nhớ ngắn hạn dài (LSTM - Long Short-Term Memory) — là quyết định kiến trúc bắt buộc để giải quyết bài toán mô hình hóa chuỗi .

Ý tưởng cốt lõi của thuật toán là tiêu thụ luồng sự kiện (view, click, add_to_cart) đã được thu thập ở Bước trước theo từng mốc thời gian để duy trì và cập nhật một trạng thái ẩn. Nhờ cơ chế các cổng logic bên trong cell (Forget, Input, Output gates), thuật toán LSTM có khả năng học được độ phụ thuộc dài hạn (long-term dependency). Nó sẽ tự động tính toán để giữ lại các tín hiệu có trọng số chuyển đổi cao (như hành vi đffa vào wishlist) và ép quên đi các tương tác nhiễu (như click nhầm). Trạng thái ẩn cuối cùng sẽ đóng gói toàn bộ ngữ cảnh của người dùng trong phiên đó, sau đó được đẩy qua lớp kết nối đầy đủ để xuất ra phân phối xác suất dự đoán chính xác sản phẩm tiếp theo.

## Model chi tiết

## Training

Kết quả training:

Nhận xét:

- - - - Về độ chính xác (Accuracy): Đồ thị Train Acc và Val Acc đồng pha chặt chẽ và bão hòa từ epoch 15. Kết thúc tại epoch 30, Val Acc đạt 62.33%, bám sát ngffỡng Train Acc (61.82%), chứng minh mô hình học tốt và có khả năng tổng quát hóa cao trên dữ liệu chffa biết.
            - Về hàm mất mát (Loss): Đffờng Train Loss giảm đều, trong khi Val Loss tiệm cận

và duy trì bình ổn quanh ngffỡng 2.46 - 2.50 trong 10 epoch cuối. Không xuất hiện sự phân kỳ đồ thị.

- - - - Kết luận: Hiện tượng Overfitting đã được khắc phục. Mô hình đạt trạng thái cân

bằng tối ưu, đảm bảo độ ổn định cần thiết để trích xuất và triển khai vào môi Trường thực tế của hệ thống.

## Knowledge Graph với Neo4jMô hình đồ thị

Cơ sở dữ liệu quan hệ sinh ra để bảo toàn tính toàn vẹn giao dịch (ACID), nhưng kiến trúc này lập tfíc sụp đổ về mặt hiệu năng khi phải thực thi các lệnh SQL JOIN đệ quy sâu nhằm dò tìm mối quan hệ chéo giữa khách hàng và hàng hóa. Để giải quyết bài toán truy vấn gợi ý phức tạp theo thời gian thực, AI Service bắt buộc phải từ bỏ cấu trúc dạng bảng và ánh xạ dữ liệu sang một mô hình đồ thị tri thức (Knowledge Graph) sử dụng Neo4j.

Mô hình đồ thị tri thức tại đây được thiết kế tinh gọn, bám sát vào luồng hành vi đã thu thập, bao gồm hai thành phần vật lý cốt lõi:

- - - - Node (Đỉnh - Thực thể): Hệ thống khoanh vùng thành hai loại node chính là User và Product. Các node này chỉ đóng vai trò là "chốt chặn" tham chiếu, lưu trữ định danh nguyên thủy (user_id, product_id) và một số siêu dữ liệu (metadata) cơ bản nhất được đồng bộ từ User Service và Product Service. Kiến trúc này cấm tuyệt đối việc nhân bản (replicate) toàn bộ dữ liệu gốc từ các service giao dịch sang AI Service nhằm ngăn chặn nguy cơ phình to bộ nhớ (memory bloat).

- - - - Edge (Cạnh - Mối quan hệ có hướng): Luồng dữ liệu sự kiện từ Mục 3.3.1 được tiêu thụ và đúc trực tiếp thành các cạnh liên kết. Cụ thể, một hành vi nhấp chuột sẽ khởi tạo cạnh \[:VIEW\] trỏ từ node User sang node Product. Khi giao dịch chốt đơn hoàn tất, hệ thống vạch ra một cạnh \[:BUY\] cứng. Quan trọng nhất, để phá vỡ điểm mù "khởi động lạnh", thiết kế bổ sung thêm loại cạnh \[:SIMILAR\]. Cạnh này không nối User với Product, mà nối trực tiếp node Product này với node Product khác, dựa trên mức độ tương đồng về thuộc tính

hoặc được sinh ra từ quá trình tính toán offline khi hai mặt hàng thường xuyên xuất hiện chung trong các giỏ hàng.

## Ví dụ Cypher

Đoạn mã trên định hình cơ chế hoạt động cứng: hệ thống sẽ quét xem User 1 và Product 101 đã tồn tại trên RAM chffa; nếu chffa mới cấp phát vùng nhớ tạo node mới. Tiếp đó, hệ thống vạch một cạnh \[:BUY\] nối hai đỉnh này. Việc nhúng thêm timestamp vào cạnh là thao tác kỹ thuật bắt buộc để phục vụ các thuật toán dọn dẹp dữ liệu cũ sau này, ngăn chặn tình trạng tràn bộ nhớ đồ thị

## Truy vấn gợi ý

Truy vấn trích xuất sản phẩm mục tiêu được thiết kế qua một cú pháp duyệt đffờng đi duy nhất:

Bản chất kỹ thuật của truy vấn này là một Bước nhảy hai nấc. Đầu tiên, engine quét các sản phẩm

(p) mà user đã mua. Sau đó, nó trffợt theo cạnh \[:SIMILAR\] để tìm các sản phẩm tương đồng (rec). Mệnh đề WHERE NOT đóng vai trò bộ lọc logic, loại bỏ ngay nhưng món hàng user đã mua để tránh gợi ý rác.

## RAG (Retrieval-Augmented Generation)Pipeline

Kiến trúc AI Service áp dụng kỹ thuật Truy xuất tăng cffờng (RAG - Retrieval-Augmented Generation). Thay vì ép LLM phải học thuộc lòng danh mục sản phẩm thông qua việc tinh chỉnh (fine-tuning) tốn kém, RAG đóng vai trò như một màng lọc kìm hãm sự sáng tạo của AI, ép câu trả lời phải neo chặt vào dữ liệu nội bộ có thật.

Đffờng ống xử lý của RAG phân rã luồng request thành hai pha độc lập nhằm tách biệt giới hạn tài nguyên:

- - - - Pha 1: Retrieve (Truy xuất). Khi người dùng nhập một truy vấn mờ như _"Tôi cần laptop gaming giá rẻ"_, hệ thống không đẩy thẳng câu hỏi này cho LLM. Thay vào đó, truy vấn được đi qua một mô hình Embedding để biến đổi thành một vector toán học. Hệ thống thực thi phép tìm kiếm độ tương đồng bên trong Vector Database để trích xuất ra top-K sản phẩm sát nghĩa nhất.
            - Pha 2: Generate (Sinh văn bản). Thông tin kỹ thuật thô của top-K sản phẩm vfia truy xuất

(bao gồm ID, tên, giá, thông số) được nội suy vào một prompt định dạng sẵn cùng với câu hỏi gốc của khách hàng. LLM đóng vai trò là chốt chặn cuối cùng, tiêu thụ prompt chfía ngữ cảnh này để tổng hợp ra một câu tư vấn hoàn chỉnh bằng ngôn ngữ tự nhiên.

## Vector Database

Để pha truy xuất trong kiến trúc RAG hoạt động, hệ thống không thể dùng lệnh quét chuỗi văn bản thông thường của SQL. Mọi dữ liệu phi cấu trúc như mô tả sản phẩm bắt buộc phải được chuyển đổi thành các vector nhúng (embeddings) đa chiều thông qua một mô hình ngôn ngữ lớn. Khi nhận một truy vấn đầu vào, cơ sở dữ liệu sẽ thực thi các phép toán đo lffờng khoảng cách không gian giữa vector câu hỏi và vector sản phẩm để dò tìm top-K kết quả sát nghĩa nhất.

Thay vì cấp phát một cụm cơ sở dữ liệu vector chuyên biệt (như FAISS hay ChromaDB), hệ thống lựa chọn pgvector — một phần mở rộng được tích hợp trực tiếp vào hệ quản trị PostgreSQL.

Quyết định này mang lại lợi thế tuyệt đối về sự tối giản hạ tầng. Đội ngũ vận hành tái sử dụng lại được toàn bộ kiến thức quản lý, cấu hình cluster và luồng sao lưu đã áp dụng cho các microservices khác. Về mặt truy vấn, pgvector cho phép kỹ sư thực thi một lệnh SQL duy nhất để vfia tìm kiếm độ tương đồng vector, vfia lọc các metadata truyền thống trên cùng một bảng. Khả năng gộp phẳng này loại bỏ hoàn toàn độ trễ mạng phát sinh từ việc phải gọi chéo giữa Vector Database (để lấy ID) và Relational Database (để lấy chi tiết sản phẩm).

Mặc dù giải quyết được bài toán phân mảnh dữ liệu, việc ép một hệ quản trị quan hệ (RDBMS) gánh vác các phép toán đại số tuyến tính của AI buộc hệ thống phải đối mặt với sự đánh đổi khốc liệt về tài nguyên. Các thuật toán tạo chỉ mục vector mạnh nhất hiện nay như HNSW (Hierarchical Navigable Small World) ngốn một lượng RAM khổng lồ để duy trì cấu trúc đồ thị trên bộ nhớ chính nhằm đảm bảo tốc độ truy xuất.

Hệ quả kỹ thuật là, nếu kỹ sư tận dụng chung database vật lý của Product Service để cài pgvector, luồng quét vector hạng nặng từ AI Service sẽ lập tfíc vắt kiệt CPU và RAM, trực tiếp đánh sập các luồng giao dịch CRUD lõi của hệ thống. Để bảo vệ ranh giới chịu lỗi cốt lõi của kiến trúc Microservices, database chạy pgvector bắt buộc phải được triển khai thành một node PostgreSQL vật lý hoàn toàn độc lập và giao quyền sở hfiu cho AI Service. Việc cô lập này ép hệ thống phải gánh thêm chi phí xây dựng một đffờng ống đồng bộ dữ liệu liên tục từ Product Service sang, chấp nhận trạng thái nhất quán trễ để đổi lấy sự sống còn của luồng mua sắm.

## Ví dụ

Xét một truy vấn phi cấu trúc từ người dùng: _"Tìm cho tôi laptop gaming dưới 25 triệu có RAM 16GB"_. Tiến trình xử lý tại AI Service phải đi qua 3 Bước

Bước 1: Nhúng truy vấn. Chuỗi văn bản thô lập tfíc được đẩy qua mô hình embedding để biến đổi thành một vector toán học không gian đa chiều, ví dụ: \[0.12, -0.04, 0.88, ...\].

_Bước 2: Truy xuất bằng pgvector._ AI Service thực thi một câu lệnh SQL kết hợp tính toán khoảng cách (&lt;=&gt;) trực tiếp trên PostgreSQL. Truy vấn này ép database dò tìm top 3 sản phẩm có độ tương đồng vector cao nhất, đồng thời áp dụng bộ lọc metadata filtering truyền thống để gạt bỏ các máy vffợt ngân sách:

SELECT id, name, specs, price FROM products

WHERE price <= 25000000

ORDER BY embedding &lt;=&gt; '\[0.12, -0.04, 0.88, ...\]'

LIMIT 3;

Giả sử kết quả trả về từ database là các bản ghi thô: \[{id: 101, name: "Acer Nitro 5", specs: "RAM 16GB, GTX 1650", price: 23500000}\].

_Bước 3: Bơm ngữ cảnh và sinh văn bản._ Dữ liệu kỹ thuật khô khan từ Bước 2 được nội suy vào một template prompt tĩnh. Kiến trúc sư bắt buộc phải thiết lập một chỉ thị hệ thống mang tính áp đặt nhằm giam lỏng khả năng sáng tạo của LLM: _"Bạn là nhân viên tư vấn bán hàng. Chỉ sử dụng thông tin kỹ thuật dưới đây để trả lời khách. Tuyệt đối không tự bịa thông số. \[Dữ liệu từ bước 2\]"_.

Lúc này, LLM mới đóng vai trò bộ tổng hợp ngôn ngữ, tiêu thụ khối prompt trên và nhả về chuỗi phản hồi tự nhiên: _"Chào bạn, với ngân sách dưới 25 triệu, hiện cửa hàng đang có mẫu Acer Nitro 5 giá 23.5 triệu, trang bị sẵn RAM 16GB và card GTX 1650 đáp ứng tốt nhu cầu chơi game của bạn..."_

## Kết hợp Hybrid Model

Mỗi mô hình AI độc lập đều mang một điểm mù kỹ thuật đặc thù. Thuật toán LSTM dự đoán xuất sắc chuỗi hành vi theo thời gian nhưng sẽ lập tfíc tê liệt trước các sản phẩm mới chffa có lịch sử tương tác (lỗi cold-start). Đồ thị tri thức (Knowledge Graph) bóc tách cực nhanh mối quan hệ "cùng mua", "tương đồng" nhờ nhảy dọc theo các con trỏ cạnh trên RAM, nhưng hệ thống này hoàn toàn

mù tịt về ngữ nghĩa ngôn ngữ tự nhiên. Ngược lại, kiến trúc RAG thông dịch chính xác ý định tìm kiếm mờ của khách hàng thông qua vector nhúng, song lại vfít bỏ hoàn toàn cấu trúc dữ liệu chuỗi thời gian của các lffợt click trước đó.

Triển khai đơn lẻ bất kỳ thuật toán nào sẽ trực tiếp tạo ra các đề xuất sai lệch. Để che lấp khiếm khuyết của từng mô hình, kiến trúc AI Service ép buộc phải hợp nhất chúng thành một mô hình lai (Hybrid Model).

Dưới góc độ hệ thống, điểm số đề xuất cuối cùng (Final Recommendation) cho một sản phẩm không được quyết định bởi một luồng duy nhất, mà là kết quả tổng hợp toán học qua cơ chế gán trọng số (weighted sum) từ cả ba cỗ máy:

final_score = w1 \* lstm + w2 \* graph + w3 \* rag

Bản chất kỹ thuật của phffơng trình này là việc thiết lập các van điều hướng logic (w1, w2, w3). Ví dụ, khi một khách hàng vãng lai vfia truy cập hệ thống và gõ thanh tìm kiếm, tập dữ liệu hành vi của họ bằng rỗng. Kỹ sư dữ liệu sẽ thiết lập cấu hình hạ trọng số w1 của LSTM xuống tiệm cận 0, đồng thời đẩy trần w3 của RAG để kết quả bám sát vào văn bản truy vấn. Khi phiên (session) kéo dài và dữ liệu click tích lũy đủ lớn, w1 và w2 sẽ tự động tăng lên để hệ thống chuyển dịch sang cơ chế dự đoán hành vi.

Mặc dù kiến trúc lai này tối ưu hóa độ chính xác của phễu lọc gợi ý, nó ép hạ tầng phần cứng phải gánh chịu một sự đánh đổi khốc liệt về hiệu năng và chi phí. Thay vì gọi một hàm suy luận , API của AI Service giờ đây phải đẩy request rẽ nhánh song song vào ba cụm xử lý nặng: nhân ma trận chuỗi trên GPU (LSTM), duyệt đệ quy đỉnh/cạnh (Neo4j), và quét khoảng cách không gian .

Quyết định gộp này trực tiếp làm phình to độ trễ tích lũy và ngốn sạch tài nguyên cấp phát. Để bảo vệ tính đáp ứng thời gian thực cho client, hệ thống bắt buộc phải áp dụng luồng thực thi bất đồng bộ khi gọi 3 mô hình. Đồng thời, kỹ sư phải thiết lập một ngffỡng thời gian chờ (timeout) cứng; nếu engine Graph hoặc RAG bị nghẽn do quá tải, luồng điều phối sẽ tự động cắt bỏ phần điểm số đó và tính toán final_score chỉ dựa trên kết quả trả về sớm nhất từ LSTM, chấp nhận một kết quả gợi ý thiếu chính xác tạm thời để đổi lấy sự sống còn của toàn bộ luồng giao dịch.

## Hai dạng AI ServiceRecommendation List

Danh sách gợi ý là hợp đồng đầu ra dạng mảng tĩnh của AI Service, đóng vai trò điều hướng luồng duyệt sản phẩm của khách hàng. Hệ thống không gọi API gợi ý liên tục ở mọi tương tác chuột để tránh vắt kiệt tài nguyên máy chủ. Thay vào đó, luồng suy luận điểm số chỉ được kích hoạt tại hai điểm chạm mà người dùng bộc lộ ý định mua sắm rõ ràng nhất: khi họ thực hiện lệnh tìm kiếm (search) hoặc khi nhấn thêm một mặt hàng vào giỏ (add-to-cart).

Dưới góc độ giao tiếp liên tiến trình API của luồng này được thiết lập theo chuẩn RESTful: GET

/recommend?user_id=1.

Thay vì xuất ra một tệp JSON phình to chfía tên, giá bán và đffờng dẫn hình ảnh, kiến trúc ép buộc AI Service chỉ được phép nhả về một mảng định danh (list of IDs) sản phẩm.

Mặc dù việc chỉ trả về ID buộc phía Frontend phải gánh chịu thêm độ trễ của một vòng gọi mạng sang Product Service để gộp thông tin chi tiết bằng kỹ thuật API Composition, sự đánh đổi này giải quyết dfít điểm bài toán dính chặt dữ liệu.

## Chatbot tư vấn

Khác với danh sách gợi ý tĩnh vận hành dựa trên các tín hiệu ngầm định (click, view), Chatbot tư vấn được thiết kế để trực tiếp tiêu thụ ý định mua sắm tường minh nhưng phi cấu trúc của khách hàng. Điểm nghẽn giao tiếp của phân hệ này được thiết lập cứng thông qua hợp đồng API POST

/chatbot, tiếp nhận payload đầu vào là chuỗi ngôn ngữ tự nhiên (ví dụ: "Tôi cần laptop gaming giá rẻ dưới 20 triệu").

Rquest bị ép chạy qua đffờng ống Truy xuất tăng cffờng (RAG) gồm 3 pha nghiêm ngặt:

1.  Bóc tách ý định (NLP Intent): Truy vấn thô được vector hóa bằng mô hình embedding.
2.  Truy xuất (Retrieve): Hệ thống thực thi phép tìm kiếm độ tương đồng vector (similarity search) bên trong cơ sở dữ liệu pgvector để trích xuất ra top-K sản phẩm sát nghĩa nhất hiện đang có sẵn trong kho.
3.  Sinh văn bản (Generate): Thông số kỹ thuật thực tế của top-K sản phẩm này được nội suy vào prompt để làm bối cảnh (context) ép LLM tổng hợp ra câu trả lời cuối cùng.

API này trả về duy nhất chuỗi văn bản tự nhiên (plain text) chfía lời tư vấn. . Nếu giao diện client muốn hiển thị thẻ sản phẩm đan xen trong đoạn chat, Frontend phải tự bóc tách các mã định danh (ID) được LLM trích dẫn và gọi một API Composition sang Product Service để lấy hình ảnh, giá cả.

## Triển khai AI ServiceTech stack

- - - - 1\. FastAPI (AI Service Framework)
                - Bản chất và vai trò: Framework web Python hoạt động theo cơ chế bất đồng bộ.
                - Ưu điểm: Khả năng xử lý I/O bất đồng bộ xuất sắc.
            - 2\. TensorFlow (Mô hình LSTM)
                - Bản chất và vai trò: Nền tảng học máy mã nguồn mở dùng để xây dựng, huấn luyện mạng nơ-ron. Tại phân hệ này, TensorFlow đảm nhiệm việc cài đặt thuật toán Bộ nhớ ngắn hạn dài để trích xuất quy luật từ chuỗi sự kiện hành vi (click, add_to_cart) theo thời gian tuyến tính.
            - 3\. Neo4j (Graph Database)
                - Bản chất và vai trò: Cơ sở dữ liệu đồ thị chuyên dụng. Nó tiêu thụ luồng log hành vi, đúc thành các đỉnh (User, Product) và nối bằng các cạnh (VIEW, BUY, SIMILAR). Nhiệm vụ của nó là thực thi các câu truy vấn Cypher dò tìm mối quan hệ tương đồng.
                - Ưu điểm: Tận dụng cơ chế lưu trữ hướng quan hệ vật lý. Thay vì quét bảng, thuật toán chỉ nhảy dọc theo các con trỏ trên RAM, trực tiếp bẻ gãy điểm nghẽn hiệu năng của các lệnh SQL JOIN đệ quy sâu khi phải phân tích dữ liệu chéo n-n.
                - Nhược điểm: Đánh đổi bằng không gian RAM. Neo4j ép hệ thống phải nạp toàn mạng lffới lên bộ nhớ chính. Nếu đồ thị xuất hiện các "điểm nút siêu cấp" (super-node) - ví dụ một món hàng quốc dân có hàng triệu cạnh kết nối - CPU sẽ lập tfíc bị vắt kiệt khi duyệt đffờng đi, bắt buộc kỹ sư phải cấu hình cắt tỉa truy vấn cẩn thận.
            - 4\. pgvector (Vector Database)
                - Bản chất và vai trò: Trình cắm biến PostgreSQL thành một cơ sở dữ liệu vector. Công cụ này gánh vác pha truy xuất trong kiến trúc RAG, dò tìm khoảng cách không gian giữa vector câu hỏi của người dùng và vector mô tả sản phẩm.
                - Ưu điểm: Tối giản hóa hạ tầng triển khai. Bằng cách gộp chung việc lưu trữ metadata và tính toán vector trên cùng một môi Trường SQL, kiến trúc này triệt tiêu hoàn toàn độ trễ mạng phát sinh nếu phải gọi chéo giữa một Vector DB độc lập và một RDBMS.
                - Nhược điểm: Thuật toán tạo chỉ mục vector, đặc biệt là HNSW, ăn mòn bộ nhớ khủng khiếp. Nếu thiết lập kiến trúc sai lầm bằng cách cài pgvector vào chung instance với Product Service, các lệnh quét vector hạng nặng từ AI sẽ lập tfíc đánh sập tiến trình CRUD cốt lõi của giao dịch mua sắm. Do đó, buộc phải cô lập nó sang một node PostgreSQL riêng.

## Kiến trúc

Giao tiếp Đồng bộ qua REST:

- - - - Các request mang tính phản hồi tfíc thì (như trích xuất danh sách gợi ý hay chat vấn đáp) áp dụng chuẩn giao tiếp đồng bộ qua REST API. Tuy nhiên, client từ bên ngoài mạng (như

Mobile App) tuyệt đối không được gọi thẳng vào FastAPI của AI Service. Mọi request buộc phải đi qua màng lọc API Gateway.

- - - - Tại đây, kiến trúc áp dụng mẫu thiết kế API Composition để giải quyết giới hạn của hợp

đồng dữ liệu. Do bản chất AI Service chỉ nhả về một mảng ID sản phẩm nguyên thủy để tối ưu tốc độ tính toán, API Gateway sẽ đứng ra làm API Composer. Khối này nhận mảng ID từ AI Service, sau đó gọi đồng bộ tiếp sang endpoint GET /products của Product Service để đắp thêm thông tin hiển thị (giá bán, URL hình ảnh) rồi mới trộn lại trả về cho Frontend.

Giao tiếp Bất đồng bộ qua Message Broker

- - - - Trái ngược với luồng truy vấn, luồng nạp dữ liệu nuôi AI tuyệt đối không được dùng REST API. Nếu AI Service liên tục gọi API sang Product Service để dò tìm hàng hóa mới, hoặc sang Order Service để kéo dữ liệu hành vi, nó sẽ gây ra các lệnh truy vấn chéo mạng khổng lồ, trực tiếp đánh sập database giao dịch.
            - Lời giải kiến trúc ở đây là chuyển đổi hoàn toàn sang giao tiếp bất đồng bộ qua Message

Broker (Apache Kafka). FastAPI lúc này hoạt động như một Subscriber, liên tục lắng nghe trên các kênh sự kiện dạng Publish/Subscribe.

- - - - Khi Product Service cập nhật thông số một dòng laptop mới, nó đóng vai trò nhà xuất bản

(Publisher), ném một sự kiện ProductUpdatedEvent vào Kafka. Tiến trình worker chạy ngầm của AI Service sẽ tiêu thụ sự kiện này, nhúng văn bản mô tả thành vector và ghi đè thẳng vào cơ sở dữ liệu pgvector. Tương tự, mọi cú nhấp chuột hay thao tác chốt đơn từ Order Service đều được đẩy vào queue, AI Service sẽ kéo về để khởi tạo các node và edge trên đồ thị Neo4j.

- - - - Sự đánh đổi khốc liệt của giao tiếp hướng sự kiện là bài toán nhất quán trễ. Một đôi giày

mới thêm vào kho có thể mất vài phút mới được sinh vector và xuất hiện trong kết quả gợi ý của Chatbot. Tuy nhiên, nó bẻ gãy hoàn toàn sự phụ thuộc thời gian. Nếu ai-service bị quá tải hoặc sập nguồn, dữ liệu hành vi từ khách hàng vẫn được Message Broker giữ lại an toàn trên ổ cứng. Khi AI Service được restart, nó sẽ đọc tiếp từ offset bị gián đoạn, đảm bảo không rơi rụng bất kỳ một tín hiệu huấn luyện nào mà không làm gián đoạn luồng mua sắm của E-commerce.

## Kết luận

Mặc dù kiến trúc Hybrid Model (kết hợp LSTM, đồ thị Neo4j và RAG pgvector) lấp đầy được các điểm mù thuật toán như hiện tượng "khởi động lạnh" (cold-start) hay ảo giác thông tin nó lại trực tiếp đẩy độ trễ hệ thống lên mức rủi ro. Việc bắt buộc ba cỗ máy tính toán này phải chạy song song để tổng hợp điểm số ép kỹ sư phải đffa ra các cơ chế phòng ngự cứng rắn. Áp dụng mẫu thiết kế Circuit Breaker và thiết lập timeout cắt luồng suy luận là sự đánh đổi bắt buộc: hệ thống chấp nhận trả về một danh sách gợi ý mặc định (fallback) hoặc phản hồi Chatbot trễ, tuyệt đối không để luồng chờ (thread blocking) làm sập API Gateway.

Dưới góc độ dữ liệu, AI Service chấp nhận trạng thái nhất quán trễ thông qua Message Broker, nó bfít rễ khỏi luồng giao dịch cốt lõi. AI Service chỉ đóng vai trò là một nhà cung cấp dữ liệu cấp thấp, trả về các mảng định danh (IDs) hoặc chuỗi văn bản nguyên thủy, đẩy toàn bộ gánh nặng định dạng giao diện và gộp dữ liệu (API Composition) ngược lại cho Frontend và Gateway.

Các ranh giới Bounded Context và hợp đồng API (API contracts) đã được vạch ra rõ ràng trên bản thiết kế lý thuyết. Tuy nhiên, toàn bộ mạng lffới microservices và AI này cần một nền tảng vật lý để luân chuyển dữ liệu. Chffơng 4 sẽ tiến hành lắp ghép toàn bộ các service này vào chung một hạ tầng mạng, sử dụng Nginx làm màng lọc định tuyến và Docker/Kubernetes để giải quyết bài toán đóng gói, triển khai và caling ở cấp độ container.

# CHƯƠNG 4: XÂY DỰNG HỆ THỐNG HOÀN CHỈNH

## Kiến trúc tổng thểMô hình hệ thống

Hệ thống được xây dựng theo kiến trúc microservices, mỗi service là một Django project độc lập.

- - - - API Gateway (Nginx)
            - user-service (Django)
            - product-service (Django)
            - cart-service (Django)
            - order-service (Django)
            - payment-service (Django)
            - shipping-service (Django)
            - ai-service (FastAPI)

## Nguyên tắc

- - - - Mỗi service có database riêng
            - Giao tiếp qua REST API
            - Không truy cập DB của service khác

## System ArchitectureOverview

Hệ thống ecom-final được thiết kế theo mô hình phân tán hoàn toàn, ứng dụng triệt để kiến trúc Microservices nhằm phá vỡ các giới hạn về cổ chai hiệu năng của khối Monolithic truyền thống. Thay vì nhồi nhét toàn bộ logic vào một tiến trình duy nhất, kiến trúc băm nhỏ ứng dụng thành các dịch vụ độc lập dựa trên ranh giới nghiệp vụ lõi. Việc phân rã này ép hệ thống phải gánh chịu độ phức tạp của giao tiếp qua mạng lffới, nhưng đổi lại thu về ba đặc tính hạ tầng sống còn: khả năng mở rộng độc lập, tính dễ bảo trì và khả năng cô lập lỗi để một service sập không kéo theo toàn bộ hệ thống chết chùm.

Dưới góc độ cài đặt vật lý, mỗi miền nghiệp vụ được bọc gói thành một microservice riêng biệt chạy trên nền Django REST. Tuy nhiên, nếu để client gọi trực tiếp đến từng service, kiến trúc sẽ

lập tfíc bị phá vỡ do sự dính chặt mạng lffới. Để giải quyết bài toán này, hệ thống thiết lập một API Gateway đóng vai trò màng lọc giao tiếp duy nhất. Chốt chặn trung tâm này gánh vác toàn bộ các tác vụ cắt ngang bao gồm: phân luồng truy cập, xác thực danh tính và áp đặt các chính sách bảo mật toàn cục trước khi đẩy tải xuống hệ sinh thái microservices bên dưới

## Microservice Architecture

Hệ thống được phân rã thành 6 microservices giao dịch cốt lõi dựa trên ranh giới Bounded Context của Domain-Driven Design (DDD). Việc rạch ròi các miền nghiệp vụ này ép buộc mỗi service phải sở hfiu một cơ sở dữ liệu vật lý hoàn toàn độc lập,. Cấu trúc cụ thể của 6 service được thiết lập như sau:

- - - - User Service: Đảm nhiệm toàn bộ luồng xác thực (Authentication), phân quyền (RBAC) và quản lý vòng đời tài khoản (Admin, Staff, Customer).
            - Product Service: Bọc gói logic của danh mục hàng hóa và 10 lớp sản phẩm kế thừa đa hình.
            - Cart Service: Quản lý vòng đời ngắn hạn của giỏ hàng. Khối này mang bản chất là một service lưu trữ trạng thái tạm (transient state), hứng chịu trực tiếp tần suất I/O khổng lồ từ các thao tác thêm/bớt liên tục của người dùng trước khi chốt đơn,.
            - Order Service: Trái tim của luồng giao dịch, quản lý cỗ máy trạng thái của đơn hàng. Nó

đóng vai trò trung tâm để duy trì luồng mua sắm, nhận dữ liệu từ Cart và chuẩn bị dữ liệu đẩy sang các mảng thanh toán, vận chuyển,.

- - - - Payment Service: Cô lập hoàn toàn nghiệp vụ tài chính. Nhiệm vụ duy nhất của nó là tương

tác với các cổng thanh toán bên ngoài và ghi nhận trạng thái giao dịch (Pending, Success, Failed) vào database cục bộ,.

- - - - Shipping Service: Gánh vác logic vận đơn (Processing, Shipping, Delivered). Service này

bfít rễ khỏi Order Service để ngăn chặn tình trạng thắt cổ chai hạ tầng khi hệ thống phải liên tục cập nhật tọa độ hoặc trạng thái giao hàng theo thời gian thực,.

## API Gateway

Kiến trúc hệ thống thiết lập một lớp API Gateway đóng vai trò là điểm truy cập duy nhất cho toàn bộ các request từ client.

Về mặt cài đặt vật lý, API Gateway trong hệ thống này được triển khai bằng phần mềm NGINX hoạt động dưới cơ chế reverse proxy. Khối Gateway này bfít rễ các tác vụ cắt ngang ra khỏi business logic và gánh vác 4 trách nhiệm kỹ thuật cốt lõi:

- - - - Định tuyến yêu cầu (Routing): NGINX đóng vai trò bộ điều hướng, quét đffờng dẫn (URL path) và phffơng thức của request tới, sau đó đẩy tải về đúng node mạng vật lý của microservice tương ứng một cách trong suốt với client.
            - Xử lý xác thực (Authentication) bằng JWT: Thay vì bắt 6 service bên dưới phải tự viết lại

logic kiểm tra người dùng, NGINX hoạt động như một chốt chặn kiểm duyệt ở rìa mạng. Nó xác thực chfi ký JSON Web Token (JWT) và lập tfíc từ chối các request chfía token rác hoặc hết hạn trước khi chúng kịp chạm vào các service giao dịch lõi.

- - - - Thực thi giới hạn lưu lượng và bảo mật (Rate limiting & Security policies): Gateway áp đặt các trần lưu lượng cứng để ngăn chặn tình trạng cạn kiệt tài nguyên do tấn công DDoS, đồng thời làm màng lọc thực thi các bộ quy tắc bảo mật toàn cục.
            - Ghi log và giám sát (Logging & Monitoring): Mọi luồng truy cập API đi qua gateway đều

được NGINX ghi vết tập trung. Thao tác này cung cấp nguồn dữ liệu thô sống còn để giám sát tần suất sử dụng, đo lffờng độ trễ và phát hiện điểm nghẽn hệ thống.

Mặc dù kiến trúc API Gateway này triệt tiêu hoàn toàn sự dính chặt giữa Frontend và Backend, việc gộp mọi luồng dữ liệu vào một proxy duy nhất ép hệ thống phải đối mặt với rủi ro cực lớn: NGINX biến thành điểm chết toàn hệ thống. Nếu tiến trình NGINX sụp đổ, toàn bộ E-commerce sẽ lập tfíc tê liệt dù các microservices bên dưới vẫn đang sống. Sự đánh đổi này ép buộc kỹ sư hệ thống bắt buộc phải cấu hình NGINX chạy đa bản sao đằng sau một Load Balancer ở tầng TCP/IP để đảm bảo tính sẵn sàng cao.

## Service Communication

## Containerization and Deployment

Để đảm bảo tính nhất quán tuyệt đối giữa các môi Trường, toàn bộ service trong hệ thống bắt buộc phải được đóng gói (containerized) dưới dạng các Docker image độc lập. Cơ chế cô lập này triệt tiêu hoàn toàn rủi ro xung đột thư viện chéo giữa các tiến trình. Ở pha phát triển, hệ thống sử dụng Docker Compose làm công cụ điều phối nhằm tối ưu tốc độ khởi tạo mạng lffới local. Khi triển khai lên môi Trường thực tế, kiến trúc này cho phép mở rộng linh hoạt bằng cách chuyển giao toàn bộ cụm container cho nền tảng Kubernetes quản lý. Mặc dù cấu hình Kubernetes làm tăng độ phức tạp vận hành hạ tầng, sự đánh đổi này là điều kiện tiên quyết để hệ thống đạt được năng lực tự phục hồi (auto-healing) và co giãn ngang (horizontal scaling) dưới áp lực tải thực tế.

## System Structure

## Design Principles

Kiến trúc của hệ thống ecom-final bị ràng buộc khắt khe bởi 4 nguyên tắc cốt lõi nhằm giải quyết bài toán phân mảnh tài nguyên và duy trì tính sống còn của luồng giao dịch:

- - - - Liên kết lỏng lẻo (Loose Coupling): Các microservice tuyệt đối không được phép chia sẻ chung cơ sở dữ liệu vật lý. Mọi tương tác liên tiến trình bắt buộc phải định tuyến thông qua các hợp đồng API (REST/gRPC) đồng bộ hoặc qua Message Broker bất đồng bộ. Mặc dù thiết kế này phá vỡ hoàn toàn sự phụ thuộc về mặt cấu trúc mã, hệ thống bắt buộc phải trả giá bằng độ trễ mạng tăng cao và ép kỹ sư phải giải quyết bài toán duy trì tính nhất quán dữ liệu trễ trên toàn cục.
            - Tính gắn kết cao (High Cohesion): Tuân thủ tuyệt đối nguyên tắc Đơn trách nhiệm (Single

Responsibility Principle - SRP) và Đóng chung (Common Closure Principle - CCP). Mỗi service được thiết kế để đóng gói trọn vẹn một miền nghiệp vụ duy nhất. Thiết lập này khoanh vùng rủi ro vật lý; khi một quy trình nghiệp vụ thay đổi, kỹ sư chỉ cần chỉnh sửa mã nguồn và tái triển khai đúng một service đó, triệt tiêu hoàn toàn thảm họa phải build lại toàn bộ hệ thống.

- - - - Khả năng mở rộng độc lập (Independent Scalability): Hệ thống gỡ bỏ được điểm nghẽn cổ

chai nhờ năng lực co giãn ngang ở cấp độ hàm và dịch vụ. Dưới áp lực tải đột biến của các đợt flash sale, hạ tầng có thể tự động cấp phát thêm hàng chục bản sao cho Cart Service hay AI Service để gánh tải I/O khổng lồ, trong khi các khối ít biến động như User Service vẫn giữ nguyên số lượng node tối thiểu nhằm tối ưu chi phí RAM và CPU.

- - - - Cô lập lỗi (Fault Isolation): Đây là lớp khiên vật lý bảo vệ hệ thống khỏi hiệu ứng sụp đổ dây chuyền. Việc phân rã kiến trúc ép mỗi service chạy trong một tiến trình độc lập hoàn toàn. Nếu AI Service bị cạn kiệt bộ nhớ (Memory Leak) do tính toán đồ thị quá tải, sự cố này chỉ đánh sập các container của AI. API Gateway lập tfíc ngắt mạch (Circuit Breaker) các luồng request bị kẹt, bảo toàn tài nguyên hệ thống để các module lõi như Order Service và Payment Service tiếp tục duy trì luồng chốt đơn của khách hàng.

## Security Considerations

Kiến trúc Microservices phân rã hệ thống thành nhiều điểm chạm mạng, trực tiếp làm phình to bề mặt tấn công so với mô hình nguyên khối. Để bảo vệ dữ liệu, hệ thống ecom-final thiết lập một vành đai bảo mật ba lớp dựa trên cơ chế xác thực phi trạng thái.

- - - - Xác thực tập trung tại API Gateway (Gateway Validation): Thay vì bắt từng microservice phải tự nhúng thư viện và lặp lại logic kiểm tra danh tính, NGINX API Gateway được thiết lập làm chốt chặn kiểm duyệt ở rìa mạng. Mọi request từ bên ngoài đều bị chặn lại để quét. Các request mang token rác hoặc không hợp lệ sẽ bị NGINX từ chối ngay lập tfíc (trả về mã lỗi HTTP 401/403). Thiết kế này trực tiếp bảo vệ các service giao dịch lõi ở tuyến sau khỏi nguy cơ cạn kiệt tài nguyên (CPU/RAM) khi phải xử lý các truy vấn độc hại.
            - Xác thực bằng JSON Web Token (JWT): Quản lý phiên người dùng bằng session lưu trên

bộ nhớ server sẽ lập tfíc phá vỡ khả năng co giãn ngang của hệ thống phân tán. Hệ thống bẻ gãy điểm nghẽn này bằng cách sử dụng JWT. Sau khi User Service cấp phát JWT chfía chfi ký mã hóa, token này sẽ tự đóng gói trọn vẹn thông tin định danh của khách hàng. Mặc dù JWT giải phóng database khỏi hàng ngàn luồng truy vấn xác thực lặp lại, kiến trúc này ép buộc hệ thống phải gánh chịu một sự đánh đổi về rủi ro thu hồi. Một khi JWT đã phát ra, hệ thống không thể vô hiệu hóa nó ngay lập tfíc trước thời điểm hết hạn, trữ khi kỹ sư chấp nhận hao tổn tài nguyên để duy trì thêm một danh sách đen trên Redis.

- - - - Kiểm soát truy cập dựa trên vai trò (RBAC): Ranh giới phân quyền được đẩy sâu vào không

gian bộ nhớ của từng microservice độc lập. Khi NGINX xác thực chfi ký JWT hợp lệ, nó đính kèm token này vào HTTP header và chuyển tiếp xuống các service nội bộ. Tại đây, các service (như Product Service hay Order Service) tự bóc tách payload của JWT để lấy thông tin vai trò (Admin, Staff, Customer) và kích hoạt bộ lọc RBAC. Thiết kế này cấp quyền tự trị tuyệt đối cho từng service; chúng tự quyết định có cho phép user thực thi tác vụ hay không mà hoàn toàn không cần gọi mạng ngược về User Service để xin phép, từ đó triệt tiêu triệt để độ trễ giao tiếp liên tiến trình.

## Discussion

Việc phá vỡ cấu trúc nguyên khối (Monolithic) để chuyển sang kiến trúc Microservices cung cấp cho hệ thống ecom-final năng lực mở rộng và tính linh hoạt vffợt trội ở cấp độ từng dịch vụ. Tuy nhiên, quyết định thiết kế này trực tiếp đẩy độ phức tạp từ không gian mã nguồn cục bộ ra không gian mạng lffới.

Mặc dù giải quyết triệt để bài toán thắt cổ chai hiệu năng và cô lập tài nguyên cho AI Service, thiết kế phân tán lại phát sinh điểm nghẽn mới: chi phí bảo trì luồng phối hợp giữa các service và gánh

nặng triển khai. Khi một nghiệp vụ chốt đơn hàng buộc phải chạy vắt chéo qua Order, Payment và Shipping Service, rủi ro lỗi cục bộ và độ trễ mạng là cái giá bắt buộc phải trả.

Để kìm hãm sự rủi ro sụp đổ dây chuyền này, kiến trúc ép buộc hệ thống phải áp đặt các ranh giới giao tiếp cứng rắn. Sự phức tạp trong điều phối luồng dữ liệu được kiểm soát thông qua việc chuẩn hóa toàn bộ giao thức giao tiếp (sử dụng REST API cho các lệnh gọi đồng bộ và Message Broker cho các luồng sự kiện bất đồng bộ).

Về mặt hạ tầng, gánh nặng triển khai hàng tá service đa ngôn ngữ (Django cho backend lõi, FastAPI cho AI) được giải quyết triệt để bằng kỹ thuật đóng gói container (Containerization). Lớp vỏ Docker đóng vai trò đồng nhất hóa môi Trường chạy, tạo tiền đề bắt buộc để các công cụ điều phối (Orchestrator) như Docker Compose hay Kubernetes có thể tự động hóa việc nâng hạ scale và phục hồi tiến trình lỗi trên môi Trường production mà không làm gián đoạn trải nghiệm mua sắm của khách hàng.

## API Gateway (Nginx)Vai trò

Việc phơi bày trực tiếp các microservices nội bộ ra ngoài Internet sẽ lập tfíc phá vỡ tính đóng gói của hệ thống và gây ra hiện tượng gọi mạng lắt nhắt. Để thiết lập ranh giới bảo mật, hệ thống sử dụng Nginx làm API Gateway, gánh vác 3 vai trò kỹ thuật cốt lõi như sau:

- - - - Entry point cho toàn hệ thống: Nginx hoạt động như một chốt chặn giao tiếp duy nhất đứng giữa client và hạ tầng mạng nội bộ. Thay vì client (như Mobile App hay Web) phải tự gọi phân tán đến từng service, mọi luồng giao tiếp bắt buộc phải đổ về Nginx. Cơ chế này che giấu hoàn toàn sự phân mảnh và độ phức tạp của topology mạng phía sau khỏi người dùng cuối.
            - Routing request đến đúng service: Khác với kiến trúc nguyên khối gọi hàm nội bộ, hệ thống

phân tán ép client phải biết địa chỉ mạng của từng node. Nginx bẻ gãy điểm nghẽn này bằng cơ chế định tuyến ngược (reverse proxy). Khi tiếp nhận HTTP request, Nginx tiến hành quét đffờng dẫn (URL path) và tự động điều hướng tải (proxy_pass) về đúng node mạng vật lý của service tương ứng (ví dụ: /products/ được đẩy về product-service:8001).

- - - - Xử lý authentication: Nếu ép từng microservice tự xác thực, hệ thống sẽ lãng phí tài nguyên

CPU để lặp lại logic giải mã JSON Web Token (JWT). Nginx tước bỏ gánh nặng này bằng cách thực thi kiểm duyệt danh tính ngay tại rìa mạng Mọi request mang token rác hoặc hết hạn sẽ bị Nginx từ chối lập tfíc (trả về mã HTTP 401/403) trước khi chúng kịp chạm vào để vắt kiệt tài nguyên của các tiến trình giao dịch lõi.

## Cấu hình mẫu

## Authentication (JWT)

Việc duy trì phiên người dùng bằng Session lưu trên RAM máy chủ sẽ lập tfíc phá vỡ năng lực co giãn ngang của cụm microservices. Để giải quyết, kiến trúc hệ thống chuyển sang sử dụng luồng xác thực phi trạng thái hoàn toàn bằng JWT, vận hành qua 3 pha kỹ thuật phân tách rạch ròi:

- Pha 1: Cấp phát Token. Khi client đẩy payload chfía thông tin đăng nhập, request được API Gateway định tuyến thẳng tới User Service. Tiến trình này xác thực thông tin với cơ sở dữ liệu, sau đó đóng gói định danh (User ID) và quyền hạn (Role) vào một payload, ký mã hóa bằng khóa bí mật để sinh ra JWT rồi trả về cho client.
- Pha 2: Đính kèm Token. Đối với mọi giao dịch tiếp theo như thêm vào giỏ hàng hay chốt

đơn, ứng dụng client bắt buộc phải nhúng chuỗi JWT này vào HTTP Header theo cú pháp

Authorization: Bearer &lt;token&gt;.

- Pha 3: Xác thực tại rìa mạng và Phân quyền nội bộ. Khi request chạm đến API Gateway, Nginx sẽ trực tiếp giải mã và xác thực chfi ký JWT. Các request chfía token rác, sai chfi ký hoặc quá hạn sẽ bị Nginx từ chối lập tfíc bằng mã lỗi HTTP 401/403. Thiết lập này biến Gateway thành lá chắn bảo vệ các service giao dịch tuyến sau khỏi nguy cơ cạn kiệt tài nguyên CPU do phải xử lý truy vấn độc hại. Nếu token hợp lệ, Nginx mới đẩy request xuống

mạng nội bộ. Tại đây, các service (như Order hay Payment) tự bóc tách JWT để đọc thông tin Role và thực thi phân quyền (RBAC) ngay tại bộ nhớ cục bộ. Thiết kế này cấp quyền tự trị cho các service, cho phép chúng ra quyết định truy cập mà không tốn chi phí gọi mạng ngược về User Service để xin phép.

## Giao tiếp giữa các Service

Để ngăn chặn rủi ro lỗi cục bộ biến thành thảm họa sụp đổ dây chuyền toàn hệ thống, kỹ sư không thể giả định mạng lffới luôn ổn định. Các lời gọi REST API đồng bộ bắt buộc phải được bọc bằng ba cơ chế phòng ngự cứng rắn:

- Thiết lập Timeout: Tuyệt đối không để một luồng mạng chờ đợi vô thời hạn. Mọi request gọi chéo service đều bị áp đặt một ngffỡng thời gian cứng (ví dụ 2-3 giây). Nếu vffợt quá ngffỡng này, kết nối bị ép ngắt ngay lập tfíc để giải phóng tài nguyên bộ nhớ và CPU, trả lại luồng làm việc cho API Gateway.
- Cơ chế Retry: Giải quyết các lỗi mạng chập chờn. Request bị rớt gói tin sẽ được hệ thống

tự động thứ lại. Mặc dù tăng cơ hội thành công cho giao dịch, việc lạm dụng Retry trên một service đang thực sự quá tải sẽ sinh ra lượng request khổng lồ, trực tiếp đánh sập nó (như một cuộc tấn công DDoS nội bộ). Do đó, cơ chế này phải được cấu hình giới hạn số lần thứ và kết hợp với độ trễ tăng dần.

- Ngắt mạch (Circuit Breaker): Đây là chốt chặn cách ly lỗi mức cao nhất. Khối Circuit

Breaker liên tục giám sát tỷ lệ lỗi và timeout của các lời gọi API. Khi tỷ lệ thất bại chạm ngffỡng nguy hiểm, mạch sẽ "mở" (Open state). Lúc này, hệ thống sẽ chặn đứng mọi request gfíi đến service đang lỗi, trả về thất bại ngay lập tfíc (Fail-fast) mà không cần đợi timeout. Trạng thái này cấp cho service lỗi thời gian trống để phục hồi. Đồng thời, hệ thống có thể kích hoạt hàm dự phòng (fallback function) – ví dụ, trả về dữ liệu cache cũ để duy trì trải nghiệm người dùng, thay vì báo lỗi trắng trang.

## Docker hóa hệ thốngDockerfile (Django)

## docker-compose.yml

## Luồng hệ thống (End-to-End)Use case: Mua hàng

## Sequence logic

# KẾT LUẬN

Hệ thống ecom-final được hiện thực hóa thông qua việc phá vỡ hoàn toàn cấu trúc Monolithic để chuyển dịch sang kiến trúc Microservices. Quyết định phân rã này không tuân theo các phân lớp công nghệ mà bám sát tuyệt đối vào ranh giới nghiệp vụ của Domain-Driven Design (DDD). Việc thiết lập các Không gian giới hạn (Bounded Context) độc lập với cơ sở dữ liệu vật lý riêng biệt đã bẻ gãy tình trạng dính chặt dữ liệu. Kiến trúc này ép buộc các service giao dịch cốt lõi phải từ bỏ lệnh SQL JOIN chéo mạng, thay vào đó giao tiếp thông qua hợp đồng REST API đồng bộ hoặc Message Broker bất đồng bộ. Mặc dù thiết kế này trực tiếp sinh ra độ trễ mạng và bài toán nhất quán dữ liệu trễ, nó thiết lập được màng lọc cô lập lỗi vfing chắc và cung cấp năng lực co giãn ngang độc lập cho từng phân hệ dưới áp lực tải thực tế.

Đối với bài toán tư vấn và gợi ý sản phẩm, hệ thống áp dụng chiến lược cô lập vật lý. AI Service được rút về một vùng không gian tính toán độc lập, cắt đfít hoàn toàn luồng truy xuất trực tiếp vào CSDL giao dịch nhằm ngăn chặn các phép toán nhân ma trận hay quét vector vắt kiệt tài nguyên CPU của luồng chốt đơn. Việc tích hợp ba cỗ máy (mô hình chuỗi LSTM, đồ thị tri thức Neo4j, và cơ sở dữ liệu vector pgvector) thành một Hybrid Model lấp đầy các khiếm khuyết thuật toán như hiện tượng khởi động lạnh hay ảo giác thông tin. Để ngăn chặn độ trễ suy luận làm sập API Gateway, tiến trình này bị buộc phải áp đặt cơ chế ngắt mạch (Circuit Breaker), hy sinh một phần độ chính xác để bảo toàn luồng mua sắm.

Ở tầng ranh giới mạng, Nginx đóng vai trò API Gateway, gánh vác toàn bộ các tác vụ cắt ngang như điều hướng request, xác thực chfi ký JWT và lắp ghép dữ liệu (API Composition). Chốt chặn này che giấu hoàn toàn sự phân mảnh của topology mạng nội bộ khỏi client. Gánh nặng triển khai kiến trúc đa ngôn ngữ (Django cho giao dịch, FastAPI cho AI) được giải quyết triệt để bằng công nghệ đóng gói Container (Docker). Thiết lập này tạo ra môi Trường chạy bất biến, triệt tiêu rủi ro xung đột thư viện và đóng vai trò là điều kiện tiên quyết để hệ thống có thể tích hợp với các công cụ điều phối cụm (như Kubernetes) ở giai đoạn vận hành.

Sự đánh đổi lớn nhất của kiến trúc phân tán này là sự bùng nổ về độ phức tạp trong bảo trì và gỡ lỗi. Khi một luồng mua hàng vắt chéo qua 6 service khác nhau, hệ thống chấp nhận phá vỡ tính toàn vẹn giao dịch nguyên thủy (ACID) thông qua mẫu thiết kế Saga để đổi lấy tính sẵn sàng cao Bản thiết kế kiến trúc cuối cùng giải quyết dfít điểm các giới hạn của hệ thống nguyên khối; nó cung cấp một hạ tầng đủ sửc hấp thụ các đợt tải đột biến, đồng thời tận dụng luồng dữ liệu hành vi khổng lồ để cá nhân hóa trải nghiệm người dùng thông qua các mô hình học máy.