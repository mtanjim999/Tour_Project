import React, { useState } from 'react';
import {
  Compass,
  Plus,
  MoreVertical,
  Search,
  MapPin,
  Users,
  Calendar,
  Construction,
  LogIn,
  Home as HomeIcon,
  ChevronRight,
  User,
  LogOut,
  Mail,
  Phone,
  Info,
  CheckCircle2,
  X,
  PlusCircle,
  Trash2,
  Image as ImageIcon,
  AlertTriangle,
} from 'lucide-react';

const firebaseConfig = {
  apiKey: 'YOUR_API_KEY',
  authDomain: 'YOUR_AUTH_DOMAIN',
  projectId: 'YOUR_PROJECT_ID',
  storageBucket: 'YOUR_STORAGE_BUCKET',
  messagingSenderId: 'YOUR_MESSAGING_SENDER_ID',
  appId: 'YOUR_APP_ID',
};

const INITIAL_TOURS = [
  {
    id: 1,
    name: 'মেঘের রাজ্য সাজেক ভ্যালি',
    location: 'রাঙ্গামাটি',
    image:
      'https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?auto=format&fit=crop&q=80&w=800',
    budget: '৫,৫০০',
    members: ['সাদিক', 'রাহাত'],
    maxSize: 10,
    date: '২০ মে, ২০২৪',
    description:
      'সাজেক ভ্যালির পাহাড়ের চূড়ায় মেঘের লুকোচুরি আর ভোরের সূর্যোদয় উপভোগ করুন আমাদের সাথে।',
    leader: 'সাদিক',
  },
  {
    id: 2,
    name: 'নীল জলের কক্সবাজার',
    location: 'কক্সবাজার',
    image:
      'https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?auto=format&fit=crop&q=80&w=800',
    budget: '৪,০০০',
    members: ['আরিফ', 'তানভীর', 'নিলয়'],
    maxSize: 12,
    date: '২৫ মে, ২০২৪',
    description:
      'বিশ্বের দীর্ঘতম সমুদ্র সৈকতে নীল জলে গা ভাসাতে আজই আমাদের টিমে যোগ দিন।',
    leader: 'আরিফ',
  },
];

export default function App() {
  const [page, setPage] = useState('home');
  const [user, setUser] = useState(null);
  const [tours, setTours] = useState(INITIAL_TOURS);
  const [showMenu, setShowMenu] = useState(false);
  const [showNotification, setShowNotification] = useState(null);
  const [errors, setErrors] = useState({});
  const [authForm, setAuthForm] = useState({ name: '', email: '', phone: '', password: '' });
  const [teamForm, setTeamForm] = useState({ name: '', location: '', budget: '', maxSize: '', date: '', description: '', image: '' });

  const notify = (msg) => {
    setShowNotification(msg);
    setTimeout(() => setShowNotification(null), 3000);
  };

  const validateAuth = () => {
    let newErrors = {};
    if (!authForm.email.includes('@')) newErrors.email = 'সঠিক ইমেইল দিন';
    if (authForm.phone.length < 11) newErrors.phone = 'সঠিক মোবাইল নম্বর দিন (১১ ডিজিট)';
    if (authForm.password.length < 6) newErrors.password = 'পাসওয়ার্ড অন্তত ৬ অক্ষরের হতে হবে';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleLogin = (e) => {
    e.preventDefault();
    if (validateAuth()) {
      setUser({ name: authForm.name || 'ভ্রমণকারী', email: authForm.email });
      setPage('home');
      notify('সফলভাবে লগইন হয়েছে!');
    }
  };

  const handleCreateTeam = (e) => {
    e.preventDefault();
    if (!user) {
      setPage('login');
      return;
    }
    const newTour = {
      ...teamForm,
      id: Date.now(),
      image:
        teamForm.image ||
        'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=800',
      members: [user.name],
      leader: user.name,
    };
    setTours([newTour, ...tours]);
    setPage('services');
    notify('নতুন ট্যুর টিম তৈরি হয়েছে!');
    setTeamForm({ name: '', location: '', budget: '', maxSize: '', date: '', description: '', image: '' });
  };

  const joinTeam = (tourId) => {
    if (!user) {
      setPage('login');
      return;
    }
    setTours(
      tours.map((t) => {
        if (t.id === tourId && !t.members.includes(user.name) && t.members.length < t.maxSize) {
          notify(`${t.name} টিমে যোগ দিয়েছেন!`);
          return { ...t, members: [...t.members, user.name] };
        }
        return t;
      }),
    );
  };

  const deleteTeam = (tourId) => {
    setTours(tours.filter((t) => t.id !== tourId));
    notify('টিমটি সফলভাবে মুছে ফেলা হয়েছে।');
  };

  const Navbar = () => (
    <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100 px-4 md:px-12 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3 cursor-pointer" onClick={() => setPage('home')}>
        <img
          src="https://i.ibb.co.com/4wSyKSSn/tourmate-logo-png.png"
          alt="Tourmate Logo"
          className="w-10 h-10 object-contain"
        />
        <span className="text-xl font-black bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">ট্যুরমেট</span>
      </div>

      <div className="hidden md:flex items-center gap-8 font-bold text-gray-600">
        <button onClick={() => setPage('home')} className={`hover:text-green-600 transition-colors ${page === 'home' ? 'text-green-600' : ''}`}>
          হোম
        </button>
        <button onClick={() => setPage('services')} className={`hover:text-green-600 transition-colors ${page === 'services' ? 'text-green-600' : ''}`}>
          ট্যুরসমূহ
        </button>
        <button onClick={() => setPage('about')} className={`hover:text-green-600 transition-colors ${page === 'about' ? 'text-green-600' : ''}`}>
          আমাদের সম্পর্কে
        </button>
        <button onClick={() => setPage('contact')} className={`hover:text-green-600 transition-colors ${page === 'contact' ? 'text-green-600' : ''}`}>
          যোগাযোগ
        </button>
      </div>

      <div className="flex items-center gap-3">
        {user ? (
          <div className="relative group">
            <button onClick={() => setShowMenu(!showMenu)} className="flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-full font-bold border border-green-100">
              <User className="w-4 h-4" /> {user.name}
            </button>
            {showMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white shadow-xl rounded-2xl border border-gray-100 p-2">
                <button onClick={() => { setPage('create'); setShowMenu(false); }} className="w-full text-left px-4 py-2 hover:bg-green-50 rounded-xl text-sm font-bold flex items-center gap-2">
                  <PlusCircle className="w-4 h-4" /> টিম তৈরি করুন
                </button>
                <button onClick={() => { setUser(null); setPage('home'); setShowMenu(false); }} className="w-full text-left px-4 py-2 hover:bg-red-50 text-red-600 rounded-xl text-sm font-bold flex items-center gap-2">
                  <LogOut className="w-4 h-4" /> লগআউট
                </button>
              </div>
            )}
          </div>
        ) : (
          <button onClick={() => setPage('login')} className="bg-green-600 text-white px-6 py-2 rounded-full text-sm font-bold hover:bg-green-700 transition-all shadow-lg shadow-green-200">
            লগইন / সাইন-আপ
          </button>
        )}
      </div>
    </nav>
  );

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 font-['Hind_Siliguri']">
      <Navbar />

      {showNotification && (
        <div className="fixed top-24 right-6 z-[60] bg-slate-900 text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-3 animate-in slide-in-from-right-10">
          <CheckCircle2 className="w-5 h-5 text-green-400" />
          <span className="font-bold">{showNotification}</span>
        </div>
      )}

      <main className="flex-grow">
        {page === 'home' && (
          <div className="animate-in fade-in duration-700">
            <section className="relative h-[85vh] flex items-center justify-center text-center px-6 overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=1600"
                className="absolute inset-0 w-full h-full object-cover scale-105"
                alt="Nature Background"
              />
              <div className="absolute inset-0 bg-black/40"></div>
              <div className="relative z-10 max-w-4xl">
                <h1 className="text-5xl md:text-8xl font-black text-white mb-6 leading-tight drop-shadow-2xl">
                  বাংলার রূপ,
                  <br />
                  <span className="text-green-400">আপনার চোখে।</span>
                </h1>
                <p className="text-lg md:text-2xl text-gray-100 mb-10 max-w-2xl mx-auto font-medium drop-shadow-lg">
                  বাংলাদেশের সবুজ প্রকৃতি আর নীল জলরাশি উপভোগ করুন সঠিক ভ্রমণ সঙ্গীর সাথে।
                </p>
                <div className="flex flex-wrap justify-center gap-4">
                  <button onClick={() => setPage('services')} className="bg-green-600 text-white px-10 py-4 rounded-2xl font-bold text-lg hover:scale-105 hover:bg-green-500 transition-all shadow-2xl flex items-center gap-2">
                    ট্যুর খুঁজুন <ChevronRight className="w-5 h-5" />
                  </button>
                  <button onClick={() => setPage('create')} className="bg-white text-slate-900 px-10 py-4 rounded-2xl font-bold text-lg hover:scale-105 hover:bg-gray-100 transition-all shadow-xl flex items-center gap-2">
                    টিম তৈরি করুন <Plus className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </section>

            <section className="py-20 px-6 max-w-7xl mx-auto">
              <div className="flex justify-between items-end mb-12">
                <div>
                  <h2 className="text-4xl font-black text-slate-900 mb-2">জনপ্রিয় ট্যুরসমূহ</h2>
                  <p className="text-slate-500 font-bold">প্রকৃতির কাছাকাছি যাওয়ার সেরা সুযোগ</p>
                </div>
                <button onClick={() => setPage('services')} className="text-green-600 font-bold flex items-center gap-1 hover:underline">
                  সবগুলো দেখুন <ChevronRight className="w-4 h-4" />
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {tours.slice(0, 3).map((tour) => (
                  <TourCard key={tour.id} tour={tour} onJoin={() => joinTeam(tour.id)} onDelete={() => deleteTeam(tour.id)} currentUser={user} />
                ))}
              </div>
            </section>
          </div>
        )}

        {page === 'create' && (
          <div className="max-w-3xl mx-auto py-20 px-6 animate-in slide-in-from-bottom-10">
            <div className="bg-white p-10 rounded-[3rem] shadow-xl border border-gray-100">
              <div className="flex items-center gap-4 mb-8">
                <div className="bg-green-100 p-3 rounded-2xl">
                  <PlusCircle className="w-8 h-8 text-green-600" />
                </div>
                <div>
                  <h2 className="text-3xl font-black text-slate-900">নতুন টিম যোগ করুন</h2>
                  <p className="text-slate-500 font-medium">ছবির ইউআরএল সহ বিস্তারিত তথ্য দিন</p>
                </div>
              </div>

              <form onSubmit={handleCreateTeam} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <label className="block text-sm font-bold text-slate-700 mb-2">ট্যুরের নাম</label>
                  <input
                    required
                    placeholder="উদা: সাজেক ও আলুটিলা ট্রিপ"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-bold text-slate-700 mb-2 flex items-center gap-2">
                    <ImageIcon className="w-4 h-4" /> ছবির লিংক (URL)
                  </label>
                  <input
                    placeholder="https://image-url.com/photo.jpg"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, image: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">গন্তব্য</label>
                  <input
                    required
                    placeholder="উদা: রাঙ্গামাটি"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, location: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">তারিখ</label>
                  <input
                    required
                    placeholder="উদা: ২০ জুন, ২০২৪"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, date: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">বাজেট</label>
                  <input
                    required
                    placeholder="উদা: ৫০০০"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, budget: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">সদস্য সংখ্যা</label>
                  <input
                    required
                    type="number"
                    placeholder="উদা: ১০"
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, maxSize: parseInt(e.target.value) })}
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-bold text-slate-700 mb-2">বিস্তারিত বর্ণনা</label>
                  <textarea
                    rows="4"
                    placeholder="আপনার ট্যুর প্ল্যান..."
                    className="w-full p-4 bg-slate-50 rounded-2xl border-none outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setTeamForm({ ...teamForm, description: e.target.value })}
                  ></textarea>
                </div>
                <div className="md:col-span-2 flex gap-4 pt-4">
                  <button type="submit" className="flex-1 bg-green-600 text-white py-4 rounded-2xl font-bold shadow-lg hover:bg-green-700 transition-all">
                    টিম পাবলিশ করুন
                  </button>
                  <button type="button" onClick={() => setPage('home')} className="px-8 py-4 bg-slate-100 text-slate-600 rounded-2xl font-bold">
                    বাতিল
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {page === 'services' && (
          <div className="py-20 px-6 max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-black text-slate-900 mb-4">সকল সক্রিয় টিম</h2>
              <p className="text-slate-500 font-bold">আপনার পছন্দের গন্তব্য খুঁজে নিন</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {tours.map((tour) => (
                <TourCard key={tour.id} tour={tour} onJoin={() => joinTeam(tour.id)} onDelete={() => deleteTeam(tour.id)} currentUser={user} />
              ))}
            </div>
          </div>
        )}

        {(page === 'login' || page === 'signup') && (
          <div className="flex items-center justify-center py-20 px-6 bg-slate-50 min-h-[80vh]">
            <div className="w-full max-w-md bg-white p-10 rounded-[2.5rem] shadow-2xl border border-gray-100">
              <h2 className="text-3xl font-black mb-2 text-slate-900 text-center">
                {page === 'login' ? 'আবার স্বাগতম!' : 'নতুন অ্যাকাউন্ট'}
              </h2>
              <form onSubmit={handleLogin} className="space-y-4">
                {page === 'signup' && (
                  <input
                    required
                    placeholder="পুরো নাম"
                    className="w-full p-4 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-green-500 font-bold"
                    onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })}
                  />
                )}
                <div className="space-y-1">
                  <input
                    required
                    type="email"
                    placeholder="ইমেইল"
                    className={`w-full p-4 bg-gray-50 rounded-2xl outline-none font-bold ${errors.email ? 'ring-2 ring-red-400' : 'focus:ring-2 focus:ring-green-500'}`}
                    onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
                  />
                  {errors.email && <p className="text-xs text-red-500 font-bold ml-4">{errors.email}</p>}
                </div>
                <div className="space-y-1">
                  <input
                    required
                    placeholder="মোবাইল নম্বর"
                    className={`w-full p-4 bg-gray-50 rounded-2xl outline-none font-bold ${errors.phone ? 'ring-2 ring-red-400' : 'focus:ring-2 focus:ring-green-500'}`}
                    onChange={(e) => setAuthForm({ ...authForm, phone: e.target.value })}
                  />
                  {errors.phone && <p className="text-xs text-red-500 font-bold ml-4">{errors.phone}</p>}
                </div>
                <div className="space-y-1">
                  <input
                    required
                    type="password"
                    placeholder="পাসওয়ার্ড"
                    className={`w-full p-4 bg-gray-50 rounded-2xl outline-none font-bold ${errors.password ? 'ring-2 ring-red-400' : 'focus:ring-2 focus:ring-green-500'}`}
                    onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                  />
                  {errors.password && <p className="text-xs text-red-500 font-bold ml-4">{errors.password}</p>}
                </div>
                <button className="w-full bg-green-600 text-white py-4 rounded-2xl font-bold shadow-lg hover:bg-green-700 mt-4">
                  {page === 'login' ? 'লগইন' : 'সাইন-আপ'}
                </button>
                <p className="text-center text-sm font-bold text-slate-500 pt-4">
                  {page === 'login' ? 'অ্যাকাউন্ট নেই?' : 'ইতিমধ্যে অ্যাকাউন্ট আছে?'}
                  <button type="button" onClick={() => setPage(page === 'login' ? 'signup' : 'login')} className="text-green-600 ml-1 underline">
                    {page === 'login' ? 'সাইন-আপ করুন' : 'লগইন করুন'}
                  </button>
                </p>
              </form>
            </div>
          </div>
        )}

        {page === 'about' && (
          <div className="py-20 px-6 max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-black text-slate-900 mb-8">আমাদের সম্পর্কে</h2>
            <p className="text-lg text-slate-600 leading-relaxed font-medium">
              ট্যুরমেট বাংলাদেশের প্রথম সোশ্যাল ট্রাভেল প্ল্যাটফর্ম যা ভ্রমণকারীদের একে অপরের সাথে যুক্ত করে। আমাদের লক্ষ্য হলো বাংলাদেশের পর্যটন খাতকে আরও সহজলভ্য এবং সামাজিক করা। আমরা বিশ্বাস করি একা ভ্রমণের চেয়ে দলবদ্ধভাবে ভ্রমণে আনন্দ এবং নিরাপত্তা দুই-ই বেশি।
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 text-left">
              <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <Users className="w-10 h-10 text-green-600 mb-4" />
                <h3 className="font-bold text-xl mb-2 text-slate-900">সহজ যোগাযোগ</h3>
                <p className="text-slate-500 text-sm font-medium">সরাসরি টিমের লিডারের সাথে যোগাযোগ করে প্ল্যান নিশ্চিত করুন।</p>
              </div>
              <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <CheckCircle2 className="w-10 h-10 text-green-600 mb-4" />
                <h3 className="font-bold text-xl mb-2 text-slate-900">নিরাপদ ভ্রমণ</h3>
                <p className="text-slate-500 text-sm font-medium">ভেরিফাইড মেম্বারদের সাথে গ্রুপ তৈরি করে ভ্রমণ করুন নিশ্চিন্তে।</p>
              </div>
              <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
                <Compass className="w-10 h-10 text-green-600 mb-4" />
                <h3 className="font-bold text-xl mb-2 text-slate-900">খরচ বাঁচান</h3>
                <p className="text-slate-500 text-sm font-medium">গ্রুপের মাধ্যমে যাতায়াত ও হোটেল খরচ ভাগ করে সাশ্রয় করুন।</p>
              </div>
            </div>
          </div>
        )}

        {page === 'contact' && (
          <div className="py-20 px-6 max-w-5xl mx-auto flex flex-col md:flex-row gap-12">
            <div className="flex-1">
              <h2 className="text-4xl font-black text-slate-900 mb-6">যোগাযোগ করুন</h2>
              <p className="text-slate-500 font-medium mb-8">যেকোনো জিজ্ঞাসা বা সাহায্যের জন্য আমাদের মেসেজ দিন।</p>
              <div className="space-y-4">
                <div className="flex items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <Mail className="w-6 h-6 text-green-600" />
                  <div>
                    <p className="text-xs text-slate-400 font-black uppercase">ইমেইল</p>
                    <p className="font-bold text-slate-800">support@tourmate.com.bd</p>
                  </div>
                </div>
                <div className="flex items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <Phone className="w-6 h-6 text-green-600" />
                  <div>
                    <p className="text-xs text-slate-400 font-black uppercase">হেল্পলাইন</p>
                    <p className="font-bold text-slate-800">+৮৮০ ১৭১২-৩৪৫৬৭৮</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex-[1.5] bg-white p-10 rounded-[3rem] shadow-xl">
              <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); notify('মেসেজ পাঠানো হয়েছে!'); }}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input required placeholder="আপনার নাম" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-green-500 font-bold" />
                  <input required type="email" placeholder="ইমেইল" className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-green-500 font-bold" />
                </div>
                <textarea rows="5" required placeholder="আপনার বার্তা..." className="w-full p-4 bg-slate-50 rounded-2xl outline-none focus:ring-2 focus:ring-green-500 font-bold"></textarea>
                <button className="w-full bg-green-600 text-white py-4 rounded-2xl font-bold shadow-lg hover:bg-green-700 transition-all">বার্তা পাঠান</button>
              </form>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-slate-900 text-white p-12 mt-20">
        <div className="max-w-7xl mx-auto text-center">
          <img src="https://i.ibb.co.com/4wSyKSSn/tourmate-logo-png.png" className="w-12 h-12 mx-auto mb-4 brightness-0 invert" alt="Footer Logo" />
          <p className="text-slate-400 font-medium">© ২০২৪ ট্যুরমেট বাংলাদেশ - সুন্দর আগামীর পথে একসাথে।</p>
        </div>
      </footer>
    </div>
  );
}

function TourCard({ tour, onJoin, onDelete, currentUser }) {
  const isJoined = currentUser && tour.members.includes(currentUser.name);
  const isFull = tour.members.length >= tour.maxSize;
  const isLeader = currentUser && tour.leader === currentUser.name;

  return (
    <div className="bg-white rounded-[2.5rem] border border-gray-100 overflow-hidden shadow-sm hover:shadow-2xl transition-all group flex flex-col h-full relative">
      {isLeader && (
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(); }}
          className="absolute top-4 left-4 z-20 bg-red-500/90 text-white p-2 rounded-xl hover:bg-red-600 transition-colors shadow-lg"
          title="টিম ডিলেট করুন"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      )}
      <div className="h-60 overflow-hidden relative">
        <img
          src={tour.image}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
          alt={tour.name}
          onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=800'; }}
        />
        <div className="absolute top-4 right-4 bg-white/95 backdrop-blur px-4 py-1.5 rounded-full text-xs font-bold text-green-700 shadow-sm flex items-center gap-1">
          <MapPin className="w-3 h-3" /> {tour.location}
        </div>
      </div>
      <div className="p-8 flex-grow flex flex-col text-left">
        <h3 className="text-xl font-bold text-slate-900 leading-tight mb-2">{tour.name}</h3>
        <p className="text-slate-500 text-sm mb-6 leading-relaxed line-clamp-2 font-medium">{tour.description}</p>
        <div className="flex items-center gap-3 mb-6 bg-slate-50 p-3 rounded-2xl">
          <Calendar className="w-4 h-4 text-green-600" />
          <span className="text-sm font-bold text-slate-700">{tour.date}</span>
        </div>
        <div className="flex items-center gap-2 mb-6">
          <div className="flex -space-x-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="w-8 h-8 rounded-full border-2 border-white bg-slate-200 flex items-center justify-center overflow-hidden">
                <User className="w-4 h-4 text-slate-400" />
              </div>
            ))}
            <div className="w-8 h-8 rounded-full border-2 border-white bg-green-100 text-green-700 text-[10px] font-black flex items-center justify-center">
              +{tour.members.length}
            </div>
          </div>
          <span className="text-xs font-bold text-slate-500 tracking-tight">({tour.members.length}/{tour.maxSize} সদস্য)</span>
        </div>
        <div className="mt-auto pt-6 border-t border-gray-50 flex justify-between items-center">
          <div>
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">বাজেট</p>
            <span className="text-green-600 font-black text-xl">৳ {tour.budget}</span>
          </div>
          {isJoined ? (
            <button className="bg-green-50 text-green-600 px-6 py-3 rounded-2xl text-sm font-bold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" /> যুক্ত আছেন
            </button>
          ) : isFull ? (
            <button className="bg-slate-100 text-slate-400 px-6 py-3 rounded-2xl text-sm font-bold cursor-not-allowed">টিম পূর্ণ</button>
          ) : (
            <button onClick={onJoin} className="bg-slate-900 text-white px-8 py-3 rounded-2xl text-sm font-bold hover:bg-green-600 transition-all shadow-lg">
              জয়েন করুন
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
