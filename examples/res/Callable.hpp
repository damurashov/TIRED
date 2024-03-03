//
// Callable.hpp

#if !defined(RR_UTIL_CALLABLE_HPP)
#define RR_UTIL_CALLABLE_HPP
namespace Rr {
namespace Cb {

namespace CallableImpl {

template <class...>
struct CallWrap;

template <class...>
struct CallMember;

template <class ...>
struct CallStatic;

template <class...>
struct CallVariant;

template <class Tsignature, class ...Targs, template <class ...> class TtArglist>
struct CallWrap<Tsignature, TtArglist<Targs...>> {
	using CallerType = typename Trait::MemberDecay<Tsignature>::ReturnType(*)(
		CallWrap<Tsignature, TtArglist<Targs...>> *, Targs... aArgs);  ///< Type erasure-based caller

	/// \brief Encapsulates callback invoke.
	///
	/// \details `caller` gets initialized within a class that derives `CallWrap<...>`. The class deriving `CallWrap<...>`
	/// is expected to static_cast the pointer it receives into its own type, thus getting access to the data it stores,
	/// and then perform the call using that information. The data may be a pointer to a function, or a pair of member
	/// function pointer and instance pointer, depending on the implementation.
	///
	CallerType caller;
};

/// \brief Stores a pointer to a plain function.
///
template <class Tsignature, class ...Targs, template <class ...> class TtArglist>
struct CallStatic<Tsignature, TtArglist<Targs...>> : CallWrap<Tsignature, TtArglist<Targs...>> {
	typename Trait::MemberDecay<Tsignature>::ReturnType(*staticCaller)(Targs ...aArgs);

	/// \brief Wraps the call using stored callback (`staticCaller`)
	///
	static typename Trait::MemberDecay<Tsignature>::ReturnType call(
		CallWrap<Tsignature, TtArglist<Targs...>> *aInstance, Targs...aArgs)
	{
		auto *thisInstance = static_cast<CallStatic<Tsignature, TtArglist<Targs...>> *>(aInstance);
		return thisInstance->staticCaller(aArgs...);
	}

	/// \brief Initializes the stored callback and derived `caller` field.
	void init(decltype(staticCaller) aCaller)
	{
		staticCaller = aCaller;
		this->caller = call;
	}
};

template <class Tsignature, class ...Targs, template <class ...> class TtArglist>
struct CallMember<Tsignature, TtArglist<Targs...>> : CallWrap<Tsignature, TtArglist<Targs...>> {

	/// \brief Helper stub that enables assessing how much storage a pointer to a virtual member takes.
	///
	struct Stub {
		virtual unsigned call(int,int,int,int)  ///< Virtual method's signature. A `virtual` is added, because the amount of storage may, in theory, depend on whether or not the pointer is `virtual`
		{
			return 0;
		}
	};

	/// \brief Stores data necessary for the callback
	///
	template <class Tptr, class Tinst>
	struct Cb {
		Tptr ptr;  ///< Pointer to a method
		Tinst inst;  ///< Pointer to an instance
	};

	/// \brief Template stub for creating callers at compile time. It uses type erasure to store a struct comprising
	/// a pointer to a class' member, and a pointer to an instance of the class.
	///
	template <class Tptr, class Tinst>
	static typename Trait::MemberDecay<Tsignature>::ReturnType call(
		CallWrap<Tsignature, TtArglist<Targs...>> *aInstance, Targs...aArgs)
	{
		auto *thisInstance = static_cast<CallMember<Tsignature, TtArglist<Targs...>> *>(aInstance);
		auto &cb = *reinterpret_cast<Cb<Tptr, Tinst> *>(thisInstance->cell);
		return (cb.inst->*cb.ptr)(aArgs...);
	}

	/// \brief Initialize `cell` and `caller`
	///
	template <class Tptr, class Tinst>
	void init(Tptr aPtr, Tinst aInst)
	{
		this->caller = call<Tptr, Tinst>;
		new (cell, Rr::Object()) Cb<Tptr, Tinst>{aPtr, aInst};
	}

	alignas(decltype(sizeof(int *))) unsigned char cell[sizeof(Cb<decltype(&Stub::call), Stub>)];  ///< Polymorphic cell storing call information
};

/// \brief A variant-like type that stores either an instance of `CallMember` or `CallStatic`.
template <class Tsignature, class ...Targs, template <class ...> class TtArglist>
struct CallVariant<Tsignature, TtArglist<Targs...>> {
	/// \brief Used to calculate the amount of storage required to hold all of the encapsulated types
	///
	union Variant {
		CallMember<Tsignature, TtArglist<Targs...>> callMember;
		CallStatic<Tsignature, TtArglist<Targs...>> callStatic;
	};
	alignas(decltype(sizeof(int *))) unsigned char variant[sizeof(Variant)];  ///< The storage for the callbacks

	/// \brief Invoke the stored callback
	///
	typename Trait::MemberDecay<Tsignature>::ReturnType operator()(Targs ...aArgs)
	{
		auto *callWrap = reinterpret_cast<CallWrap<Tsignature, TtArglist<Targs...>> *>(variant);
		return (callWrap->caller)(callWrap, aArgs...);  // Due to the fact that all of the stored types share the same superclass, we may be pretty sure about the memory layout
	}

	/// \brief Initializes the storage w/ a pointer to a function
	///
	CallVariant(typename Trait::MemberDecay<Tsignature>::CallbackType aCallback)
	{
		auto callStatic = new (variant, Rr::Object{}) CallStatic<Tsignature, TtArglist<Targs...>>();
		callStatic->init(aCallback);
	}

	/// \brief Initializes the storage w/ a pointer to a class' method and the pointer to that class.
	///
	template<class Tinstance>
	CallVariant(typename Trait::MemberDecay<Tsignature, Trait::Stript<Tinstance>>::CallbackType aCallback, Tinstance aInstance)
	{
		static_assert(sizeof(aCallback) + sizeof(aInstance) < sizeof(CallMember<Tsignature, TtArglist<Targs...>>), "");  // Redundant check to make sure that everything fits
		auto callMember = new (variant, Rr::Object{}) CallMember<Tsignature, TtArglist<Targs...>>();
		callMember->init(aCallback, aInstance);
	}
};

}  // namespace CallableImpl

template <class Tsignature>
using Callable = typename CallableImpl::CallVariant<Tsignature, typename Trait::MemberDecay<Tsignature>::ArgsList>;

}  // namespace Cb
}  // namespace Rr

#endif // RR_UTIL_CALLABLE_HPP
